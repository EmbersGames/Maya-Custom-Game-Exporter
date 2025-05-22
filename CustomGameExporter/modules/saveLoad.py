import maya.cmds as cmds

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

SetNumber = 1
PrefixList = []
ExportSetList = []

ClipNumber = 1
ClipName = []
ClipStart = []
ClipEnd = []

Path = ""


def launch_save(SetList, ClipList, ExportPath):
    save_sets_data(SetList)
    save_clip_data(ClipList)
    save_path(ExportPath)

    save_in_fileinfo()

def launch_load():

    load_from_fileinfo()




def save_sets_data(SetList):
    
    global SetNumber 
    SetNumber = len(SetList)

    PrefixList.clear()
    ExportSetList.clear()

    for Row in SetList:
        Prefix = Row.itemAt(1).widget().text()
        ExportSet = Row.itemAt(2).widget().currentText()

        PrefixList.append(Prefix)
        ExportSetList.append(ExportSet)
    
    print("Sets save completed")


def save_clip_data(ClipList):
    
    global ClipNumber 
    ClipNumber = len(ClipList)

    ClipName.clear()
    ClipStart.clear()
    ClipEnd.clear()

    for Row in ClipList:
        Name = Row.itemAt(1).widget().text()
        Start = Row.itemAt(2).widget().text()
        End = Row.itemAt(3).widget().text()

        ClipName.append(Name)
        ClipStart.append(Start)
        ClipEnd.append(End)
    
    print("Clip save completed")


def save_path(ExportPath):

    global Path
    Path = ExportPath.text()

    print("Path save completed")




def save_in_fileinfo():
    cmds.fileInfo("GE_SetNumber", SetNumber)
    convert_List_info_and_save("GE_SetPrefix", PrefixList)
    convert_List_info_and_save("GE_SetExportSet", ExportSetList)

    cmds.fileInfo("GE_ClipNumber", ClipNumber)
    convert_List_info_and_save("GE_ClipName", ClipName)
    convert_List_info_and_save("GE_ClipStart", ClipStart)
    convert_List_info_and_save("GE_ClipEnd", ClipEnd)

    cmds.fileInfo("GE_Path", Path)

    print("Save in file info completed")


def load_from_fileinfo():
    global SetNumber
    global PrefixList 
    global ExportSetList 

    global ClipNumber 
    global ClipName 
    global ClipStart 
    global ClipEnd

    global Path


    SetNumber = int(cmds.fileInfo("GE_SetNumber", query=True)[0])
    PrefixList = load_List_info("GE_SetPrefix")
    ExportSetList = load_List_info("GE_SetExportSet")

    ClipNumber = int(cmds.fileInfo("GE_ClipNumber", query=True)[0])
    ClipName = load_List_info("GE_ClipName")
    ClipStart = load_List_info("GE_ClipStart")
    ClipEnd = load_List_info("GE_ClipEnd")

    Path = cmds.fileInfo("GE_Path", query = True)[0]


    AllInfo = str(SetNumber) + str(PrefixList) + str(ExportSetList) + str(ClipNumber) + str(ClipName) + str(ClipStart) + str(ClipEnd)
    print("Load from file info completed: " + AllInfo)




def convert_List_info_and_save(FileInfoName, Obj):
    
    ConvertedString = str(Obj)
    ConvertedString = ConvertedString.replace("[", "")
    ConvertedString = ConvertedString.replace("]", "")
    ConvertedString = ConvertedString.replace("'","")

    cmds.fileInfo(FileInfoName, ConvertedString)



def load_List_info(FileInfoName):

    LoadedInfo = cmds.fileInfo(FileInfoName, query = True)[0]

    LoadedInfoList = LoadedInfo.split(", ")

    return LoadedInfoList
    
