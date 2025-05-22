import maya.cmds as cmds

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . import ui


class AddExportSetRow:

    def __init__(self, Prefix=None, ExportSet=None, LayoutSet=None, SetList=None):
        self.add_row(Prefix, ExportSet, LayoutSet, SetList)


    def add_row(self, Prefix=None, ExportSet=None, LayoutSet=None, SetList=None, Index=-1):

        Row_ExportSet = QHBoxLayout()

        Button_DeleteExportSetRow = QPushButton()
        Button_DeleteExportSetRow.setIcon(QIcon(ui.icon_path("TrashCan.png")))
        Button_DeleteExportSetRow.setFixedSize(35 , 35)
        Button_DeleteExportSetRow.clicked.connect(lambda: self.delete_row(Row_ExportSet, SetList))

        TextField_Prefix = QLineEdit()
        TextField_Prefix.setPlaceholderText("Prefix")
        TextField_Prefix.setText(Prefix)
        TextField_Prefix.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        DropDown_ExportSet = QComboBox()
        DropDown_ExportSet.addItems(self.list_export_sets())
        DropDown_ExportSet.addItem("Selection...")
        if ExportSet is not None:
            DropDown_ExportSet.setCurrentText(ExportSet)
        DropDown_ExportSet.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        

        CheckBox_Export = QCheckBox()
        CheckBox_Export.setChecked(True)

        Button_AddRowAbove = QPushButton()
        Button_AddRowAbove.setFixedSize(20,35)
        Button_AddRowAbove.setText("+")
        Button_AddRowAbove.clicked.connect(lambda: self.add_row_above(LayoutSet, SetList, Row_ExportSet))


        Row_ExportSet.addWidget(Button_DeleteExportSetRow)
        Row_ExportSet.addWidget(TextField_Prefix)
        Row_ExportSet.addWidget(DropDown_ExportSet)
        Row_ExportSet.addWidget(CheckBox_Export)
        Row_ExportSet.addWidget(Button_AddRowAbove)
        
        if Index == -1:
            SetList.append(Row_ExportSet)
        else:
            SetList.insert(Index-1, Row_ExportSet)


        LayoutSet.insertLayout(Index, Row_ExportSet)



    def delete_row(self, Row, List):
        List.remove(Row)

        while Row.count():
            item = Row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        Row.deleteLater()
    

    def list_export_sets(self):

        sets = cmds.ls(sets=True)

        # specific_word = "deformer"
        # setlist = [s for s in sets if specific_word in s]

        return sets
    
    def add_row_above(self, Layout, List, CurrentRow):
        Index = Layout.indexOf(CurrentRow)
        self.add_row(None, None, Layout, List, Index)
        
    


class AddAnimClipRow:
    def __init__(self, ClipName=None, Start=None, End=None, Layout_AnimClip=None, ClipList=None):
        self.add_row(ClipName, Start, End, Layout_AnimClip, ClipList)



    def add_row(self, ClipName=None, Start=None, End=None, Layout_AnimClip=None, ClipList=None, Index=-1):
        Row_AnimClip = QHBoxLayout()

        start_time = cmds.playbackOptions(q=True, min=True)
        end_time = cmds.playbackOptions(q=True, max=True)
        ConvertStart = int(start_time)
        ConvertEnd = int(end_time)

        Button_DeleteClip = QPushButton()
        Button_DeleteClip.setIcon(QIcon(ui.icon_path("TrashCan.png")))
        Button_DeleteClip.setFixedSize(35 , 35)
        Row_AnimClip.addWidget(Button_DeleteClip)
        Button_DeleteClip.clicked.connect(lambda: self.delete_row(Row_AnimClip, ClipList))
        # Button_DeleteClip.clicked.connect(self.debug)

        self.TextField_ClipName = QLineEdit()
        self.TextField_ClipName.setPlaceholderText("Clip name...")
        self.TextField_ClipName.setText(ClipName)
        Row_AnimClip.addWidget(self.TextField_ClipName)


        TextField_TimeStart = QLineEdit()
        if Start is not None:
            TextField_TimeStart.setText(str(Start))
        else:
            TextField_TimeStart.setText(str(ConvertStart))
        TextField_TimeStart.setFixedWidth(45)
        Row_AnimClip.addWidget(TextField_TimeStart)

        TextField_TimeEnd = QLineEdit()
        if End is not None:
            TextField_TimeEnd.setText(str(End))
        else:
            TextField_TimeEnd.setText(str(ConvertEnd))
        TextField_TimeEnd.setFixedWidth(45)
        Row_AnimClip.addWidget(TextField_TimeEnd)

        Button_Playback = QPushButton()
        Button_Playback.setIcon(QIcon(ui.icon_path("FilmStrip.png")))
        Button_Playback.setFixedSize(35 , 35)
        Button_Playback.clicked.connect(lambda: self.set_playback(Row_AnimClip))
        Row_AnimClip.addWidget(Button_Playback)

        CheckBox_Export = QCheckBox()
        CheckBox_Export.setChecked(True)
        Row_AnimClip.addWidget(CheckBox_Export)

        Button_AddRowAbove = QPushButton()
        Button_AddRowAbove.setFixedSize(20,35)
        Button_AddRowAbove.setText("+")
        Button_AddRowAbove.clicked.connect(lambda: self.add_row_above(Layout_AnimClip, ClipList, Row_AnimClip))
        Row_AnimClip.addWidget(Button_AddRowAbove)

        if Index == -1:
            ClipList.append(Row_AnimClip)
        else:
            ClipList.insert(Index-1, Row_AnimClip)

        Layout_AnimClip.insertLayout(Index, Row_AnimClip)

        
    
    def delete_row(self, Row, List):
        List.remove(Row)

        while Row.count():
            item = Row.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        Row.deleteLater()

    def set_playback(self, Row):
        Start = Row.itemAt(2).widget().text()
        End = Row.itemAt(3).widget().text()
        cmds.playbackOptions(min=Start, max=End)
    
    def add_row_above(self, Layout, List, CurrentRow):
        Index = Layout.indexOf(CurrentRow)
        self.add_row(None, None, None, Layout, List, Index)


    
    def debug(self):
        self.list_anim_layer()



class AddAnimLayerRow():
    def __init__(self, MasterLayout, ClipName, Index=-1):
        self.LayerList = self.query_animLayer()

        self.add_row(MasterLayout, ClipName, Index)

    def add_row(self, MasterLayout, ClipName, Index):
        self.AnimLayer_Layout = QHBoxLayout()

        self.Anim_ClipName = QLineEdit()
        self.Anim_ClipName.setReadOnly(True)
        self.Anim_ClipName.setMaximumWidth(250)
        self.Anim_ClipName.setPlaceholderText("Clip name...")
        self.Anim_ClipName.setText(ClipName)
        self.AnimLayer_Layout.addWidget(self.Anim_ClipName)

        for layer in self.LayerList:
            self.checkbox_by_layer(self.AnimLayer_Layout, layer)


        MasterLayout.insertLayout(Index, self.AnimLayer_Layout)

        ui.separator_stretch(self.AnimLayer_Layout, 50)
        

    def query_animLayer(self):
        RootLayer = cmds.animLayer(query=True, root=True)
        Layers = cmds.animLayer(RootLayer, query=True, children=True)

        return Layers
    
    def checkbox_by_layer(self, Layout, LayerName):

        self.CheckBox = QCheckBox()
        self.CheckBox.setChecked(False)
        self.CheckBox.setText(LayerName)
        Layout.addWidget(self.CheckBox)


    def delete_row(self):

        while self.AnimLayer_Layout.count():
            item = self.AnimLayer_Layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.AnimLayer_Layout.deleteLater()

