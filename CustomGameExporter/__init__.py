import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.OpenMaya as OpenMaya

from . import main, CallbacksData

callbacks = []

def add_callbacks(win):
	global callbacks
	callbacks.append(OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kBeforeSave, win.save_data))
	callbacks.append(OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterOpen, win.load_when_new_scene))
	callbacks.append(OpenMaya.MSceneMessage.addCallback(OpenMaya.MSceneMessage.kAfterNew, win.load_when_new_scene))

	CallbacksData.CallbackList = callbacks


def run():
	
	global win, callbacks

	open_windows = cmds.lsUI(windows=True)
	for obj in open_windows:
		if obj.find("UISetup_GameExporterCustom") != -1:
			cmds.deleteUI(obj)

	win = main.UISetup_GameExporterCustom()
	win.show(dockable = True)

	add_callbacks(win)
      

run()
