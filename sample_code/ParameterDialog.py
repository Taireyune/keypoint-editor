#%%
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5 import QtWidgets
from utils import utils
from config import ConfigConstants
from config.Language import language as LG
from globalObjects import GlobalData
import numpy as np
import pickle

class ParameterDialog:
    def __init__(self):
        super(ParameterDialog, self).__init__()

        self.parameter_dialog = QtWidgets.QDialog()
        self.parameter_dialog.setObjectName("parameter_dialog")
        self.parameter_dialog.resize(610, 500)
        self.parameter_dialog.setWindowTitle(LG("camera parameters"))
        self.parameter_dialog.setWindowIcon(QIcon(utils.get_path(["iconImages", "PyroVision.png"])))

        self.mainLayout = QtWidgets.QVBoxLayout(self.parameter_dialog)
        self.mainLayout.setObjectName("mainLayout")

        ########Full text label: rolling shutter########
        self.textExplain1 = QtWidgets.QTextEdit(self.parameter_dialog)
        self.textExplain1.setObjectName("textExplain1")
        self.textExplain1.setText(LG("camera text"))
        self.textExplain1.setMinimumSize(QSize(605, 80))
        self.textExplain1.setMaximumSize(QSize(605, 80))
        self.textExplain1.setReadOnly(True)
        self.textExplain1.setStyleSheet("QTextEdit {background-color: rgb(240, 240, 240);}")
        self.mainLayout.addWidget(self.textExplain1)

        ########selected calibration########
        # self.calibrationObject = subject_found[0]
        # self.calibrationMethod = QtWidgets.QLabel(self.calibration_dialog)
        # self.calibrationMethod.setObjectName("calibrationMethod")
        # self.calibrationMethod.setText("calibration method: " + self.calibrationObject.name + " 2D calibration")
        # self.calibrationMethod.setFont(QFont('MS Shell Dlg 2', 10))
        # self.calibrationMethod.setAlignment(Qt.AlignCenter)
        # self.mainLayout.addWidget(self.calibrationMethod)

        ########cmo rolling shutter parameters########

        ########Scan Direction###########
        self.rollingType = QtWidgets.QHBoxLayout()
        self.rollingType.setObjectName("rollingType")

        #Description for combo box
        self.typeLabel = QtWidgets.QLabel(self.parameter_dialog)
        self.typeLabel.setObjectName("typeLabel")
        self.typeLabel.setText(LG("choose scan direction"))
        self.typeLabel.setMinimumSize(QSize(480, 32))
        self.typeLabel.setMaximumSize(QSize(480, 32))
        self.rollingType.addWidget(self.typeLabel)

        # #spacer
        # spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.rollingType.addItem(spacerItem1)

        #combo box
        self.typeComboBox=QtWidgets.QComboBox(self.parameter_dialog)
        self.typeComboBox.setMinimumSize(QSize(125, 26))
        self.typeComboBox.setMaximumSize(QSize(125, 26))
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItems(["top to bottom", "left to right", "bottom to top", "right to left"])         
        #self.typeComboBox.activated[str].connect(self.ComboMode)
        self.rollingType.addWidget(self.typeComboBox)

        self.mainLayout.addLayout(self.rollingType)

        ###########Time to scan##########
        self.scanTime = QtWidgets.QHBoxLayout()
        self.scanTime.setObjectName("scanTime")

        #Description for text edit 1
        self.editLabel1 = QtWidgets.QLabel(self.parameter_dialog)
        self.editLabel1.setObjectName("editLabel1")
        self.editLabel1.setText(LG("scanning duration"))
        self.editLabel1.setMinimumSize(QSize(480, 32))
        self.editLabel1.setMaximumSize(QSize(480, 32))
        self.scanTime.addWidget(self.editLabel1)

        # #spacer
        # spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.scanTime.addItem(spacerItem2)

        #Text edit for scan time
        self.scanTimeText = QtWidgets.QPlainTextEdit(self.parameter_dialog)
        self.scanTimeText.setMinimumSize(QSize(80, 28))
        self.scanTimeText.setMaximumSize(QSize(80, 28))
        self.scanTimeText.setObjectName("scanTimeText")
        self.scanTimeText.appendPlainText(str(round(GlobalData.cmoParameter["scanDuration"]*1000, 3)))
        self.scanTime.addWidget(self.scanTimeText)
        #self.stickLength.setEnabled(False)

        #Unit label for text edit 1
        self.editUnit1 = QtWidgets.QLabel(self.parameter_dialog)
        self.editUnit1.setObjectName("editUnit1")
        self.editUnit1.setText("ms")
        self.editUnit1.setMinimumSize(QSize(40, 32))
        self.editUnit1.setMaximumSize(QSize(40, 32))
        self.scanTime.addWidget(self.editUnit1)

        self.mainLayout.addLayout(self.scanTime)

        ########Time between scan########
        self.gapTime = QtWidgets.QHBoxLayout()
        self.gapTime.setObjectName("gapTime")

        #Description for time between scan
        self.editLabel2 = QtWidgets.QLabel(self.parameter_dialog)
        self.editLabel2.setMinimumSize(QSize(480, 32))
        self.editLabel2.setMaximumSize(QSize(480, 32))
        self.editLabel2.setObjectName("editLabel2")
        self.gapTime.addWidget(self.editLabel2)
        self.editLabel2.setText(LG("scanning gap"))

        # #spacer
        # spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.gapTime.addItem(spacerItem3)

        #Text edit for gap time
        self.gapTimeEdit = QtWidgets.QPlainTextEdit(self.parameter_dialog)
        self.gapTimeEdit.setMinimumSize(QSize(80, 28))
        self.gapTimeEdit.setMaximumSize(QSize(80, 28))
        self.gapTimeEdit.setObjectName("gapTimeEdit")
        self.gapTimeEdit.appendPlainText(str(round(GlobalData.cmoParameter["scanGap"]*1000, 3)))
        self.gapTime.addWidget(self.gapTimeEdit)
        #self.blCoordinateX.setEnabled(False)

        #Unit label for gap time
        self.editUnit2 = QtWidgets.QLabel(self.parameter_dialog)
        self.editUnit2.setObjectName("editUnit2")
        self.editUnit2.setText("ms")
        self.editUnit2.setMinimumSize(QSize(40, 32))
        self.editUnit2.setMaximumSize(QSize(40, 32))
        self.gapTime.addWidget(self.editUnit2)

        self.mainLayout.addLayout(self.gapTime)

        ########spacing#########
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(spacerItem)

        ########save calibration or quit dialog#######
        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.buttonsLayout.setObjectName("buttonsLayout")
        self.saveBtn = QtWidgets.QPushButton(self.parameter_dialog)
        self.saveBtn.setMinimumSize(QSize(300, 28))
        self.saveBtn.setMaximumSize(QSize(300, 28))
        self.saveBtn.setObjectName("saveBtn")
        self.saveBtn.clicked.connect(self.saveSettings)
        self.saveBtn.setText(LG("save"))
        self.buttonsLayout.addWidget(self.saveBtn)

        self.cancelBtn = QtWidgets.QPushButton(self.parameter_dialog)
        self.cancelBtn.setMinimumSize(QSize(300, 28))
        self.cancelBtn.setMaximumSize(QSize(300, 28))
        self.cancelBtn.setObjectName("cancelBtn")
        self.cancelBtn.clicked.connect(self.cancel_Btn)
        self.cancelBtn.setText(LG("cancel"))
        self.buttonsLayout.addWidget(self.cancelBtn)
        self.mainLayout.addLayout(self.buttonsLayout)


    # def ComboMode(self, mode):
    #     GlobalData.cmoParameter["type"] = mode

    def saveSettings(self, event):
        GlobalData.cmoParameter["type"] = str(self.typeComboBox.currentText())
        GlobalData.cmoParameter["scanDuration"] = float(self.scanTimeText.toPlainText())/1000
        GlobalData.cmoParameter["scanGap"] = float(self.gapTimeEdit.toPlainText())/1000
        self.parameter_dialog.close()

    def cancel_Btn(self):
        self.parameter_dialog.close()

    
        

