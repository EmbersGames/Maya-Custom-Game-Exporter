import os

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

grey_black = "rgb(45,45,45)"
grey_dark = "rgb(65,65,65)"
grey_light = "rgb(85,85,85)"
grey_clear = "rgb(130,130,130)"
orange_light = "#db9456"
orange_dark = "#816146"
line_height = 45
red_warning = "rgb(125, 60, 60)"


class SeparatorWidget(QtWidgets.QFrame):
	def __init__(self,parent=None, color=grey_light,Height = 4, Width = 4):
		super(SeparatorWidget, self).__init__()
		self.setStyleSheet(f"QFrame {{background-color: {color};}}")
		self.setFrameShape(QtWidgets.QFrame.HLine)
		self.setMinimumHeight(Height)
		self.setMinimumWidth(Width)
		self.setContentsMargins(1,1,1,1)


def icon_path(IconName):
	module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	icon_path = os.path.join(module_dir, "icons", IconName)
	return icon_path


def title_label(Layout, Text = str):
	Title = QLabel(Text)
	Title.setAlignment(Qt.AlignCenter)
	Title.setFont(QFont.setBold(True))

	Layout.addWidget(Title)

def clear_layout(Row):

	# Clear all widgets in the layout
	while Row.count():
		item = Row.takeAt(0)
		widget = item.widget()
		if widget:
			widget.deleteLater()
	Row.deleteLater()

	# print("Delete complete")



def separator_stretch(Layout, Value=20):
		Layout.addSpacing(Value)
		Layout.addStretch()
        
