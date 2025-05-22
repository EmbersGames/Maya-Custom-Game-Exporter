# Maya - Custom Game Exporter for animator
A custom version of Maya's GameExporter tailored for animation.

## Installation
Clone the repository and place the *"CustomGameExporter"* folder in your Maya scripts directory.\
\
In the Maya Script Editor, run the following command:
```python
import importlib

import CustomGameExporter
importlib.reload(CustomGameExporter)
```
Feel free to add this command in a shelf button for easier access.

# Functionalities
## Anim tab
![AnimTab](/ReadMeImage/I_AnimTab.png)
The anim tab is the main tab of the exporter.\
It replicates the core functionalities of the original GameExporter, with one major difference:

### Sets
You can create multiple **"Sets"**, each with a unique prefix.\
The exporter will export all selected animation clips for every set you have created.
This is particularly useful when you have multiple characters in a scene and want to export a custom fbx for all of them at once.\
\
The "Set" dropdown menu lists all sets present in your scene.\
To define a Set, create a *"Quick Selection Set"* that includes all the elements you want to export—typically all the deformer bones of the character.\
If you don't want to use sets, you can use the *"Selection..."* option to export the current selection manually.



### Path
The Path defines the folder where the exported FBX files will be saved.\
You can browse and select a folder by clicking the "Path" button.\
\
If the selected path is relative to the project folder, it will appear in the text field as:
*"[...]/your/folder"*, where *"[...]/"* represents the project root path.\
If the path is outside the project, the text field will display the absolute path instead.\
\
It is recommended to use project-relative paths to avoid issues when working in a team environment.

### Dialog window
A custom dialog window is located at the bottom of the exporter.\
It displays various messages, such as save/load warnings, export overwrites, and other important information.

## Anim layers tab
![AnimTab](/ReadMeImage/I_AnimLayerTab.png)
This tab allows you to export your animation clips with specific animation layers.\
\
For each animation clip created in the *"Anim"* tab, you can specify which animation layers should be active during export.\
When the export is triggered, the exporter will automatically mute any unchecked animation layers.

## Batch export tab
![AnimTab](/ReadMeImage/I_BatchTab.png)
This tab allows you to export multiple scenes in a batch process.\
It will export all animation clips from every scene located in a specified folder.\
\
**WARNING:** Batch export only works with scenes that use this Custom Game Exporter.


