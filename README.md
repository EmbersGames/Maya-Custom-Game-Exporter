# Maya Custom Game Exporter for animator.
A custom version of Maya's GameExporter tailored for animation.

## Installation
Clone the repository and place the CustomGameExporter folder in your Maya scripts directory.\
In Maya script editor, type the following command:
```python
import importlib

import CustomGameExporter
importlib.reload(CustomGameExporter)
```
Feel free to add this command in a shelf button for easier access.

# Functionnalities
## Anim tab
The anim tab is the main tab of the exporter.\
It reproduce the main functionnalities of the original GameExporter with one major difference:\
You can add multiple "Sets" which have all a unique prefix.\
The exporter will export every selected animation clips for every sets you have created.
This is useful when you have multiple characters in your scene and you want to export the same animation for all the characters.
