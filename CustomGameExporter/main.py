import os

import maya.cmds as cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMaya as OpenMaya

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys

from . import version, CallbacksData, BatchExport
from .modules import directory, FBXExport, saveLoad, row, exportSettings, ui

SetList = []
ClipList = []
LayerListInfo = []


class UISetup_GameExporterCustom(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UISetup_GameExporterCustom, self).__init__(parent)

        self.initUI()
        self.button_connect()
        # self.load_data()
        try:
            self.load_when_new_scene()
        except:
            self.write_in_debug("###  WARNING: LOADING ERROR  ###")
            print("Loading main error")


    def hideEvent(self, event):

        for cb_id in CallbacksData.CallbackList:
            OpenMaya.MMessage.removeCallback(cb_id)

        CallbacksData.CallbackList.clear()
        print("Deleting callbacks completed")
        

    def initUI(self):

        self.setWindowTitle(version.Name)
        self.setGeometry(100, 100, 650, 600)

        global Layout_ExportSet
        global Layout_AnimClip
        global Layout_AnimLayer

        MainTab = QTabWidget()
        AnimTab = QWidget()
        AnimLayerTab = QWidget()
        BatchTab = QWidget()


        # Create anim layout
        AnimMainLayout = QVBoxLayout()

        Widget_ExportSet = QWidget()
        Widget_AnimClip = QWidget()
        Widget_ExportZone = QWidget()

        AnimMainLayout.addWidget(ui.SeparatorWidget())
        AnimMainLayout.addWidget(Widget_ExportSet)
        AnimMainLayout.addSpacing(50)
        AnimMainLayout.addWidget(ui.SeparatorWidget())
        AnimMainLayout.addWidget(Widget_AnimClip)
        AnimMainLayout.addStretch()
        AnimMainLayout.addSpacing(10)
        AnimMainLayout.addWidget(ui.SeparatorWidget())
        AnimMainLayout.addWidget(Widget_ExportZone)
        AnimMainLayout.addSpacing(10)



        # Export set zone
        Layout_ExportSet = QVBoxLayout(Widget_ExportSet)

        Button_AddExportSetRow = QPushButton("Add set")
        Button_AddExportSetRow.clicked.connect(lambda: row.AddExportSetRow(None, None, Layout_ExportSet, SetList))
        Layout_ExportSet.addWidget(Button_AddExportSetRow)

        row.AddExportSetRow(None, None, Layout_ExportSet, SetList)



        # Anim clip zone
        Layout_AnimClip = QVBoxLayout(Widget_AnimClip)

        Widget_AnimClip_Button = QWidget()
        HLayout_AnimClip_Button = QHBoxLayout(Widget_AnimClip_Button)
        Layout_AnimClip.addWidget(Widget_AnimClip_Button)


        Button_AddAnimClipRow = QPushButton("Add clip")
        Button_AddAnimClipRow.clicked.connect(self.add_anim_clip)
        HLayout_AnimClip_Button.addWidget(Button_AddAnimClipRow)






        # Export zone
        self.Layout_ExportZone = QVBoxLayout(Widget_ExportZone)
        self.Layout_ExportZone_Path = QHBoxLayout()
        self.Layout_ExportZone_Export = QHBoxLayout()
        self.Layout_ExportZone_DebugText = QHBoxLayout()
        
        
        self.TextField_Path = QLineEdit()
        self.Layout_ExportZone_Path.addWidget(self.TextField_Path)
        self.Button_Path = QPushButton("Path")
        self.Layout_ExportZone_Path.addWidget(self.Button_Path)
        
        if version.Dev:
            self.Button_Debug = QPushButton("Debug")
            self.Layout_ExportZone_Export.addWidget(self.Button_Debug)
        # self.Button_Settings = QPushButton("Settings")
        # self.Layout_ExportZone_Export.addWidget(self.Button_Settings)
        self.Button_Export = QPushButton("Export")
        self.Button_Export.setStyleSheet(f"background-color:{ui.orange_dark}")
        self.Layout_ExportZone_Export.addWidget(self.Button_Export)


        self.Debug_TextField = QTextEdit()
        self.Debug_TextField.setReadOnly(True)
        self.Debug_TextField.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.Layout_ExportZone_DebugText.addWidget(self.Debug_TextField)


        self.Layout_ExportZone.addLayout(self.Layout_ExportZone_Path)
        self.Layout_ExportZone.addLayout(self.Layout_ExportZone_Export)
        self.Layout_ExportZone.addSpacing(20)
        self.Layout_ExportZone.addLayout(self.Layout_ExportZone_DebugText)
        self.Layout_ExportZone.addSpacing(20)
        self.Layout_ExportZone.addStretch()

        ##########################

        MasterLayout_Layers = QVBoxLayout()
        Widget_LayerZone = QWidget()
        Widget_Layers_Export = QWidget()

        MasterLayout_Layers.addWidget(ui.SeparatorWidget())
        MasterLayout_Layers.addWidget(Widget_LayerZone)
        MasterLayout_Layers.addStretch()
        MasterLayout_Layers.addWidget(Widget_Layers_Export)
        MasterLayout_Layers.addSpacing(10)

        Layout_AnimLayer = QVBoxLayout(Widget_LayerZone)
        self.Button_Refresh_Layers = QPushButton("Refresh layers")
        Layout_AnimLayer.addWidget(self.Button_Refresh_Layers)

        Layout_AnimLayer_02 = QVBoxLayout(Widget_Layers_Export)
        self.Layers_Export_Button = QPushButton("Export with layer settings")
        self.Layers_Export_Button.setStyleSheet(f"background-color:{ui.orange_dark}")
        Layout_AnimLayer_02.addWidget(self.Layers_Export_Button)


        ##########################

        BatchLayout = QVBoxLayout()

        TutoText = QTextEdit()
        TutoText.setReadOnly(True)
        TutoText.setStyleSheet("background-color: rgb(50, 50, 50);")
        TutoText.setText(BatchExport.read_tuto())
        BatchLayout.addWidget(TutoText)

        self.Button_LaunchBatch = QPushButton("Launch batch")
        self.Button_LaunchBatch.setStyleSheet(f"background-color:{ui.orange_dark}")
        BatchLayout.addWidget(self.Button_LaunchBatch)


        #########################

        AnimTab.setLayout(AnimMainLayout)
        AnimLayerTab.setLayout(MasterLayout_Layers)
        BatchTab.setLayout(BatchLayout)
        MainTab.addTab(AnimTab, "Anim")
        MainTab.addTab(AnimLayerTab, "Anim layers")
        MainTab.addTab(BatchTab, "Anim Batch Export")



        # Create window 
        MainLayout = QVBoxLayout()
        MainLayout.addWidget(MainTab)
        self.setLayout(MainLayout)

    def button_connect(self):
        self.Button_Path.clicked.connect(self.set_directory)
        self.Button_Export.clicked.connect(self.launch_export)
        # self.Button_Settings.clicked.connect(exportSettings.UISetup)

        ########################

        self.Button_Refresh_Layers.clicked.connect(self.refresh_layers_info)
        self.Layers_Export_Button.clicked.connect(self.launch_export_from_layers)

        ########################

        self.Button_LaunchBatch.clicked.connect(BatchExport.run)
        
        if version.Dev:
            self.Button_Debug.clicked.connect(self.debug_launch)


 ##############################################



    def add_anim_clip(self):

        row.AddAnimClipRow(None, None, None, Layout_AnimClip, ClipList)


    def get_anim_clip_info(self, Clip):
        ClipName = Clip.itemAt(1).widget().text()
        Start = Clip.itemAt(2).widget().text()
        End = Clip.itemAt(3).widget().text()
        Checkbox = Clip.itemAt(5).widget()

        return ClipName, Start, End, Checkbox
    
    def get_anim_layer_info(self, LayerRow):
        ClipName = LayerRow.itemAt(0).widget().text()

        for i in range(LayerRow.count()):
            widget = LayerRow.itemAt(i).widget()
            if isinstance(widget, QCheckBox):
                if widget.isChecked():
                    LayerListInfo.append(widget.text())
        
        return ClipName
    
    def refresh_layers_info(self):
        
        for obj in Layout_AnimLayer.children():
            ui.clear_layout(obj)
        
        try:
            for clip in ClipList:
                ClipName = self.get_anim_clip_info(clip)[0]

                row.AddAnimLayerRow(Layout_AnimLayer, ClipName)
        except:
            print("Can't create layers info. Check if there are layers in the scene.")
            self.write_in_debug("Can't create layers info. Check if there are layers in the scene.")

    def mute_anim_layer(self, Index):
        LayerListInfo.clear()
        LayerList = cmds.ls(type="animLayer")
        RootLayer = cmds.animLayer(query=True, root=True)
        LayerList.remove(RootLayer)
        
        self.get_anim_layer_info(Layout_AnimLayer.children()[Index])
        

        for layer in LayerList:

            if layer in LayerListInfo:
                cmds.animLayer(layer, edit=True, mute=False)
                print("j'ai activé" + layer)
            else:
                cmds.animLayer(layer, edit=True, mute=True)
                print("j'ai mute" + layer)

###############################################


    def set_directory(self):
        PathToSearch =  self.TextField_Path.text()
        ProjectPath = cmds.workspace(q=True, rootDirectory=True)
        if "[...]/" in PathToSearch:
            PathToSearch = PathToSearch.replace("[...]/", ProjectPath)

        self.Path = directory.InitBrowseFolder(PathToSearch)
        if self.Path:
            self.TextField_Path.setText(self.Path)
        else:
            pass

    def launch_export(self, UseLayers = False):
        FilePathText = self.TextField_Path.text()
        PlaybackStart = cmds.playbackOptions(q=True, min=True)
        PlaybackEnd = cmds.playbackOptions(q=True, max=True)

        #Retreive the correct file path from project folder
        ProjectPath = cmds.workspace(q=True, rootDirectory=True)

        self.save_data()

        if "[...]/" in FilePathText:
            FilePath = FilePathText.replace("[...]/", ProjectPath)
        else:
            FilePath = FilePathText

        for Set in SetList:
            ExportSetCheckbox = Set.itemAt(3).widget()

            if ExportSetCheckbox.isChecked():
                for idx, Clip in enumerate(ClipList):
                    Prefix = Set.itemAt(1).widget().text()
                    
                    ExportSet = Set.itemAt(2).widget().currentText()
                    if ExportSet == "Selection...":
                        ExportSet = cmds.ls(selection = True)

                    ClipName, Start, End, Checkbox = self.get_anim_clip_info(Clip)

                    FileName = (Prefix + ClipName)

                    if Checkbox.isChecked():
                        #setup anim layers
                        if UseLayers:
                            # print("Je désactive les layers")
                            self.mute_anim_layer(idx)
                        else:
                            # print("nik les layers")
                            pass

                        #launch export
                        cmds.select(ExportSet)
                        cmds.playbackOptions(min=Start, max=End)
                        FinalPath = FBXExport.exportFBX(FilePath, FileName, Start, End)

                        if FinalPath[0]:
                            self.write_in_debug(FileName + " has been overwritten.")

        print(FilePath)
        cmds.playbackOptions(min=PlaybackStart, max=PlaybackEnd)
            
    def launch_export_from_layers(self):

        self.launch_export(UseLayers=True)

###############################################

    def save_data(self, *args):
        saveLoad.launch_save(SetList, ClipList, self.TextField_Path)

        self.write_in_debug("Game Exporter save completed.")
        print("GE Save completed")

    def load_data(self, *args):

        saveLoad.launch_load()

        # Clear all the row before recreating them 
        SetToDelete = Layout_ExportSet.children() + Layout_AnimClip.children()
        SetList.clear()
        ClipList.clear()

        for obj in SetToDelete:
            ui.clear_layout(obj)




        # Create new rows with stocked data
        for obj in range(saveLoad.SetNumber):
            row.AddExportSetRow(
                saveLoad.PrefixList[obj],
                saveLoad.ExportSetList[obj],
                Layout_ExportSet,
                SetList
            )

        for obj in range(saveLoad.ClipNumber):
            row.AddAnimClipRow(
                saveLoad.ClipName[obj],
                saveLoad.ClipStart[obj],
                saveLoad.ClipEnd[obj],
                Layout_AnimClip, 
                ClipList
                )

        # Set the correct path   
        self.TextField_Path.setText(saveLoad.Path)

        # Refresh layer tab
        self.refresh_layers_info()
        
        self.write_in_debug("Game Exporter load completed.")
        print("Load completed")
   
    def load_when_new_scene(self, *args):
        

        try:
            self.load_data()
        except:
            SetToDelete = Layout_ExportSet.children() + Layout_AnimClip.children()
            SetList.clear()
            ClipList.clear()


            for obj in SetToDelete:
                obj.deleteLater()


            row.AddExportSetRow(None, None, Layout_ExportSet, SetList)
            row.AddAnimClipRow(None, None, None, Layout_AnimClip, ClipList)
            self.TextField_Path.setText("")


            self.refresh_layers_info()

            print("No info to load")


###############################################


    def write_in_debug(self, TextToWrite):
        self.Debug_TextField.append(TextToWrite)

    def debug_launch(self):
        pass
        