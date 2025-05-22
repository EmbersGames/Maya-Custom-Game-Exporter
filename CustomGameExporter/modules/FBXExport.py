import maya.cmds as cmds
import maya.mel as mel
import os

def getFBXSettings():
    # get current user settings for FBX export and store them
    output = mel.eval("FBXPushSettings;")
    print("output is :" + str(output))


def setFBXSettings():
    # set user-defined FBX settings back after export
    mel.eval("FBXPopSettings;")

def exportFBX(exportFilePath, exportFileName, min_time, max_time):

    FinalExportName = exportFilePath + "/" + exportFileName + ".fbx"
    IsOverwrite = os.path.exists(FinalExportName)
    # store current user FBX settings
    getFBXSettings()

    # export selected as FBX
    # Geometry
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v false")
    mel.eval("FBXExportSmoothMesh -v false")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportReferencedAssetsContent -v false")
    mel.eval("FBXExportAnimationOnly -v false")
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval("FBXExportBakeComplexStart -v " + str(min_time))
    mel.eval("FBXExportBakeComplexEnd -v " + str(max_time))
    mel.eval("FBXExportBakeComplexStep -v 1")
    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportQuaternion -v euler")
    mel.eval("FBXExportShapes -v false")
    mel.eval("FBXExportSkins -v false")
    # Constraints
    mel.eval("FBXExportConstraints -v false")
    # Cameras
    mel.eval("FBXExportCameras -v false")
    # Lights
    mel.eval("FBXExportLights -v false")
    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")
    # Connections
    mel.eval("FBXExportInputConnections -v false")
    mel.eval("FBXExportIncludeChildren -v true")
    # Axis Conversion
    mel.eval("FBXExportUpAxis y")
    # Version
    mel.eval("FBXExportFileVersion -v FBX201600")
    mel.eval("FBXExportInAscii -v true")

    # cmds.FBXProperties()

    cmds.file(FinalExportName, exportSelected=True, type="FBX export", force=True, prompt=False)

    # restore current user FBX settings
    setFBXSettings()
    
    return IsOverwrite, FinalExportName
