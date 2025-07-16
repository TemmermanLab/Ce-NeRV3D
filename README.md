**_Ce_-NeRV3D Blender Add-on**

•	This tool allows you to generate high-quality images or videos of your genes of interest within the _C. elegans_ nervous system.

•	To use this add-on, you'll need the following:
1.	Blender (https://www.blender.org/download/)
2.	The Python add-on file
3.	NeRV3D.blend
4.	A .csv file (in the shared folder we included two versions of the CeNGEN dataset)

**Installation guidelines:**

•	Download and install Blender
•	Open the software and select Edit-->Preferences…-->Add-ons-->Install and select the NeRV3D.py file provided in the folder, select Install Add-on and you should get the file in the list like this (remember to check the box otherwise the add-on will not appear in your blender view). 

<img width="382" height="302" alt="image" src="https://github.com/user-attachments/assets/ce8f96a7-a7f9-4d89-80bf-972b76356991" />

•	Close this window and now go on File-->Open and select NeRV3D.blend

•	You’ll see a window like this:
1.	Left Panel: This contains a list of Collections, including the cameras used for different render angles and a transparent cuticle.
At this stage, all Collections should be enabled—make sure both the eye and camera icons are visible.

_If any are disabled now, neurons may not appear during gene selection later._

2.	Right Panel: You’ll find a toolbar labeled Item, Tool, View, and Custom Tools. The Custom Tools tab corresponds to the add-on you’ve just installed.

<img width="452" height="180" alt="image" src="https://github.com/user-attachments/assets/9f0c7dbe-90a0-412a-80dd-d4fc6b6afb55" />

**Step 1: Load the CSV file**

•	Start by selecting the .csv file containing your gene expression data. The folder includes two preformatted CeNGEN files.
You can also load other datasets (e.g., from Calico), but they must follow the same structure—that is, the same column and row format as the CeNGEN files. The Python script is designed to recognize this specific structure.

•	To load your file:
1.	In the Custom Tool panel, click Load CSV.
2.	Copy and paste the full file path into the box.
Example: /Users/blender/NeRV3D/021821_medium_threshold2.csv
3.	Click OK. Your CSV should now load properly.
   
**Step 2: Select Genes of Interest**

•	Once the CSV is loaded, you can start selecting genes:
1.	In the Custom Tool panel, choose Gene.
2.	Enter a gene name using CeNGEN nomenclature (e.g., _flp-1_).
3.	Click OK, then select Select By Gene.
•	Only enter one gene at a time. To select multiple genes, repeat this process for each gene individually
•	Selected genes will appear in the left panel as new neuron objects. These are copies of the original neurons, so you can safely delete them later without affecting the base model.
Step 3: Hide Non-Selected Neurons
•	To view only the neurons expressing your selected gene(s), click Toggle Invisible. This will hide all other Collections.

<img width="140" height="149" alt="image" src="https://github.com/user-attachments/assets/32b93870-8b8c-442d-84d0-6c606e24f94a" />

**Optional: Show Transparent Cuticle**

•	If you want to include the transparent cuticle in your scene:
1.	In the left panel, click the closed eye icon next to Cuticle_transparent to make it visible.
2.	Make sure the camera icon is also enabled, or the cuticle won't appear in the final render.

<img width="448" height="20" alt="image" src="https://github.com/user-attachments/assets/955dbf60-3582-4d24-9a76-64c5b4f19bb4" />

**Customize your visualization:**

•	The first step in customizing your visualization is changing the color of the neurons expressing your gene of interest. 

•	To do this select one of the neurons associated with your gene, like this:

<img width="452" height="53" alt="image" src="https://github.com/user-attachments/assets/b9aa976c-6054-476a-99f5-23d56db6a8da" />

•	Next, go to the 3-Material tab. In the right-hand panel, you’ll see the material assigned to your selected gene—along with its current color (randomly assigned by default). 
You can easily change this color to one of your choice here.

<img width="165" height="224" alt="image" src="https://github.com/user-attachments/assets/50691cbd-7153-4f03-9bd5-5599e609959f" />

•	In this example, all neurons expressing flp-1 are colored magenta by default. 

To change the color:
1.	Click on Base Color and choose any shade you prefer.
2.	Click OK, and all neurons expressing your gene of interest will update to the new color.
   
•	You can repeat this process for each gene you've selected to create your own custom color palette.

**Select a Camera for Rendering**

•	You can choose from static cameras for still images or a rotating camera for video rendering.

•	Click on 2-Model in the left panel to view and select from the available camera options.

<img width="452" height="128" alt="image" src="https://github.com/user-attachments/assets/1ddfa8ae-180e-48d8-8051-7bd8389377ab" />

•	To select a camera, simply click on the green camera icon next to the one you want to use. The only camera designed for video rendering is the "Rotating Camera", which follows a predefined path and performs a full 360° rotation around the worm.

•	If you’d like to customize your camera angles, you can move existing cameras to new positions or add multiple cameras as needed.
•	To ensure you're viewing through the active camera, switch to the Camera Perspective by pressing 0 on your keypad.

_If you switch to a different view, simply press 0 again to return to the camera view._

<img width="452" height="74" alt="image" src="https://github.com/user-attachments/assets/c6033f4c-87e5-4b28-aac4-b242b506529c" />

**Adjust Output Resolution**

•	Go to the Layout tab.
•	In the lower-right panel, you'll find settings for:
1.	Resolution (X and Y): Adjust the image or video dimensions.
2.	Frames Per Second (FPS): Set the frame rate for video. A value of 25 fps is typically ideal.
3.	Output Folder: Choose the destination for saving your rendered files.
   
_Note: Changing the resolution (X and Y values) may affect your camera framing. After adjusting the resolution, double-check that the correct portion of the worm is still visible in the camera view._

**Generate Your Render**
•	Go to the Render menu in the top toolbar.
•	Choose Render Image to generate a still image.
•	Choose Render Animation to create a video.

<img width="163" height="312" alt="image" src="https://github.com/user-attachments/assets/a8e33619-67bd-49d9-b36c-5662ebe50c73" />
