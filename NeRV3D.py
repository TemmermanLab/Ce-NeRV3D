import os
import sys
import shutil

from bpy.types import Context

sys.path.append(os.path.dirname(__file__))

import bpy
import csv
import random

random.seed(42)

bl_info = {
    "name": "NeRV3D",
    "author": "Golinelli L., Cambareri V.",
    "blender": (3, 0, 0),
    "version": (0, 1),
    "location": "Leuven, Belgium",
    "description": "NeRV3D - Transcriptional Reporter Prediction",
    "category": "3D Visualization",
}


class CelData:
    def __init__(self):
        self.file_path = None

    def load_data(self, file_path):
        self.file_path = file_path
        if os.path.exists(self.file_path):
            read_data = self._read_csv()
            self.neurons = read_data[0][3:]
            self.genes = [read_data[_][1] for _ in range(1, len(read_data))]
            self.matrix = [read_data[_][3:] for _ in range(1, len(read_data))]
            self.selected = None
        return

    def _read_csv(self):
        def try_float(value):
            try:
                return float(value)
            except ValueError:
                return value

        # Open the CSV file and create a CSV reader object
        with open(self.file_path, "r") as file:
            csv_reader = csv.reader(file)

            # Iterate through each row in the CSV file
            all_rows = []
            for row in csv_reader:
                # Convert each value in the row to a numeric type (float)
                numeric_row = [try_float(value) for value in row]
                all_rows.append(numeric_row)
        return all_rows


cel = CelData()


class WM_OT_LoadCSV(bpy.types.Operator):
    bl_idname = "wm.load_csv"
    bl_label = "LoadCSV"
    text: bpy.props.StringProperty(name="Load CSV", default="")

    def execute(self, context):
        t = self.text
        pname = os.path.join(os.path.dirname(__file__), "current.csv")
        shutil.copyfile(t, pname)
        cel.load_data(pname)
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class MESH_OT_SelectByGene(bpy.types.Operator):
    bl_idname = "mesh.select_by_gene"
    bl_label = "SelectByGene"

    def execute(self, context):
        gene_names = cel.selected

        for g in gene_names:
            try:
                hits = [
                    _[0] for _ in enumerate(cel.matrix[cel.genes.index(g)]) if _[1] > 0
                ]
                found = True
                selected_neurons = [cel.neurons[_] for _ in hits]
            except Exception as ex:
                print(f"{__class__} Exception: {ex}")
                found = False

            if found:
                # We will need a deselect all button that restores properties I guess.
                bpy.ops.object.select_all(action="DESELECT")

                for n in selected_neurons:
                    bpy.ops.object.select_pattern(
                        pattern=f"{n}*", case_sensitive=True, extend=True
                    )

                collection = bpy.data.collections.new(g)
                mat = bpy.data.materials.new(name=g)
                mat.diffuse_color = (
                    random.uniform(0, 1),
                    random.uniform(0, 1),
                    random.uniform(0, 1),
                    1.0,
                )
                bpy.context.scene.collection.children.link(collection)
                for _ in bpy.context.selected_objects:
                    copied_obj = _.copy()
                    copied_obj.name = _.name + f"_{g}"
                    copied_obj.data.materials[0] = mat
                    collection.objects.link(copied_obj)

        return {"FINISHED"}


class WM_OT_TextOp(bpy.types.Operator):
    bl_label = "Gene Selector"
    bl_idname = "wm.textop"
    text: bpy.props.StringProperty(name="Select Gene:", default="flp-1")

    def execute(self, context):
        t = self.text
        cel.selected = [t]
        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class OBJ_OT_SetCollectionsInvisible(bpy.types.Operator):
    bl_label = "Toggle Invisible"
    bl_idname = "object.set_collections_invisible"

    def execute(self, context):
        # Iterate through all collections
        for collection in bpy.data.collections:
            if collection.name not in cel.genes:
                collection.hide_render = not collection.hide_render
                collection.hide_viewport = not collection.hide_viewport
        return {"FINISHED"}


class OBJ_OT_SetTransparentCuticle(bpy.types.Operator):
    bl_label = "Transparent Cuticle"
    bl_idname = "object.set_transparent_cuticle"

    def execute(self, context):
        for collection in bpy.data.collections:
            for _ in collection.objects:
                if _.name in ["Cuticle"]:
                    transp_cuticle = _.copy()

                    mat = bpy.data.materials.new("Transparent")
                    mat.use_nodes = True
                    nodes = mat.node_tree.nodes

                    # clear all nodes to start clean
                    for node in nodes:
                        nodes.remove(node)

                    # link nodes
                    links = mat.node_tree.links

                    # create the basic material nodes
                    node_output = nodes.new(type="ShaderNodeOutputMaterial")
                    node_output.location = 400, 0
                    node_pbsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
                    node_pbsdf.location = 0, 0
                    node_pbsdf.inputs["Base Color"].default_value = (
                        0.9,
                        0.85,
                        0.85,
                        0.2,
                    )
                    node_pbsdf.inputs[
                        "Alpha"
                    ].default_value = 0.2  # 1 is opaque, 0 is invisible
                    node_pbsdf.inputs["Roughness"].default_value = 0.0
                    node_pbsdf.inputs["Specular"].default_value = 0.0
                    node_pbsdf.inputs[
                        "Transmission"
                    ].default_value = 0.0  # 1 is fully transparent

                    link = links.new(
                        node_pbsdf.outputs["BSDF"], node_output.inputs["Surface"]
                    )

                    mat.blend_method = "HASHED"
                    mat.shadow_method = "HASHED"
                    mat.use_screen_refraction = True

                    bpy.context.scene.eevee.use_ssr = True
                    bpy.context.scene.eevee.use_ssr_refraction = True

                    transp_cuticle.name = _.name + "_transparent"
                    transp_cuticle.hide_render = False
                    transp_cuticle.hide_viewport = False
                    transp_cuticle.data.materials.clear()
                    transp_cuticle.data.materials.append(mat)
                    collection.objects.link(transp_cuticle)
                    break
        return {"FINISHED"}


class VIEW3D_PT_SelectionQuery(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Custom Tool"
    bl_idname = "VIEW3D_PT_SelectionQuery"
    bl_category = "Custom Tools"

    def draw(self, context):
        layout = self.layout
        rowsub = layout.row()
        rowsub.operator("wm.textop", text="Gene")
        rowsub0 = layout.row()
        rowsub0.operator("wm.load_csv", text="Load CSV")
        rowsub1 = layout.row()
        rowsub1.operator("mesh.select_by_gene", text="Select By Gene")
        rowsub2 = layout.row()
        rowsub2.operator("object.select_all", text="Select All")
        rowsub3 = layout.row()
        rowsub3.operator("object.set_collections_invisible", text="Toggle Invisible")
        rowsub3 = layout.row()
        rowsub3.operator("object.set_transparent_cuticle", text="Transparent Cuticle")


classes = (
    WM_OT_TextOp,
    WM_OT_LoadCSV,
    MESH_OT_SelectByGene,
    VIEW3D_PT_SelectionQuery,
    OBJ_OT_SetCollectionsInvisible,
    OBJ_OT_SetTransparentCuticle,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
