import os

import maya.cmds as cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys

from . import ui



class UISetup(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UISetup, self).__init__(parent)

        self.initUI()
        self.button_connect()
        self.show()

    
    
    def initUI(self):

        self.setWindowTitle("WindowName")
        self.setGeometry(100, 100, 650, 600)

        # Create Main Layout and Main Widget
        mainLayout = QVBoxLayout()

        Widget_Settings = QWidget()
        Widget_Button = QWidget()


        mainLayout.addWidget(ui.SeparatorWidget())
        mainLayout.addWidget(Widget_Settings)
        mainLayout.addSpacing(50)
        mainLayout.addWidget(ui.SeparatorWidget())
        mainLayout.addWidget(Widget_Button)
        mainLayout.addStretch()
        mainLayout.addSpacing(10)

        # Settings list
        SettingsLayout = QVBoxLayout(Widget_Settings)

        ui.title_label(SettingsLayout, "Geometry")
        self.setting_row_boolean(SettingsLayout, "Smoothing Groups")
        self.setting_row_boolean(SettingsLayout, "Export Hard Edges")
        self.setting_row_boolean(SettingsLayout, "Export Tangents")
        self.setting_row_boolean(SettingsLayout, "Export Smooth Mesh")
        self.setting_row_boolean(SettingsLayout, "Export Instances")
        self.setting_row_boolean(SettingsLayout, "Export Referenced Assets Content")
        self.setting_row_boolean(SettingsLayout, "Export Animation Only")
        self.setting_row_boolean(SettingsLayout, "Export Bake Complex Animation")
        self.setting_row_boolean(SettingsLayout, "Export Use Scene Name")
        self.setting_row_boolean(SettingsLayout, "Export Export Shapes")
        self.setting_row_boolean(SettingsLayout, "Export Export Skins")

        

        # Create window 
        self.setLayout(mainLayout)


    def setting_row_boolean(self, ParentLayout, Text = str):
        Row = QHBoxLayout()
        Row.addWidget(QLabel(Text))
        Row.addWidget(QCheckBox())
        
        ParentLayout.addLayout(Row)

    def button_connect(self):
        pass