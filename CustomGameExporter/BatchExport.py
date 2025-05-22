import maya.cmds as cmds
import maya.mel as mel
import os

from . import main



def run():
	win = main.UISetup_GameExporterCustom()

	DebugSceneList = []

	ProjectPath = cmds.workspace(q=True, rd=True)
	SceneFolder = cmds.fileDialog2(dialogStyle=1, fileMode=3, dir=ProjectPath)[0]

	SceneList = os.listdir(SceneFolder)


	for obj in range(len(SceneList)):
		CurrentScene = os.path.join(SceneFolder, SceneList[obj])

		cmds.file(CurrentScene, open = True, force=True)

		win.load_when_new_scene()
		win.launch_export()

		DebugSceneList.append(SceneList[obj])

	cmds.file(new=True, force=True)

	for obj in DebugSceneList:
		print(obj)

def read_tuto():
	FolderName = "Ref"
	FileName = "BatchExportTuto.txt"

	TutoPath = os.path.join(os.path.dirname(__file__), FolderName, FileName)

	with open(TutoPath, 'r') as file:
		content = file.read()
	
	return content