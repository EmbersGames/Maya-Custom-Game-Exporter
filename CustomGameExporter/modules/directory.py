import os

import maya.cmds as cmds

ProjectPath = cmds.workspace(q=True, rootDirectory=True)
CurrentFileName = cmds.file(query = True, expandName = True)
CurrentFolder = os.path.dirname(CurrentFileName)
ParentFolder = os.path.dirname(CurrentFolder)


def BrowseFolder(Directory):
    try:
        FolderPath = cmds.fileDialog2(dialogStyle=1, fileMode=3, dir=Directory)[0]
        try:
            ReturnPath = FolderPath.replace(ProjectPath, "[...]/")
        except:
            ReturnPath = FolderPath
    except:
        ReturnPath = ""
        print("No Path")

    return ReturnPath

def InitBrowseFolder(TextFieldDirectory):
    if not TextFieldDirectory: 
        ReturnPath = BrowseFolder(ProjectPath)
    else:
        ReturnPath = BrowseFolder(TextFieldDirectory)

    return ReturnPath
