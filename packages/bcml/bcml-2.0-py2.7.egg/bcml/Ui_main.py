# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\macad\Documents\Git\BCML-2\.vscode\main.ui',
# licensing of 'c:\Users\macad\Documents\Git\BCML-2\.vscode\main.ui' applies.
#
# Created: Sun Jul 28 14:56:18 2019
#      by: pyside2-uic  running on PySide2 5.12.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(8)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnInstall = QtWidgets.QPushButton(self.centralwidget)
        self.btnInstall.setObjectName("btnInstall")
        self.horizontalLayout_3.addWidget(self.btnInstall)
        self.btnRemerge = QtWidgets.QPushButton(self.centralwidget)
        self.btnRemerge.setObjectName("btnRemerge")
        self.horizontalLayout_3.addWidget(self.btnRemerge)
        self.btnChange = QtWidgets.QPushButton(self.centralwidget)
        self.btnChange.setEnabled(False)
        self.btnChange.setObjectName("btnChange")
        self.horizontalLayout_3.addWidget(self.btnChange)
        self.btnExport = QtWidgets.QPushButton(self.centralwidget)
        self.btnExport.setEnabled(False)
        self.btnExport.setObjectName("btnExport")
        self.horizontalLayout_3.addWidget(self.btnExport)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMaximumSize(QtCore.QSize(276, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(-1, 3, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblImage = QtWidgets.QLabel(self.groupBox)
        self.lblImage.setText("")
        self.lblImage.setScaledContents(True)
        self.lblImage.setObjectName("lblImage")
        self.verticalLayout.addWidget(self.lblImage)
        self.lblModInfo = QtWidgets.QLabel(self.groupBox)
        self.lblModInfo.setObjectName("lblModInfo")
        self.verticalLayout.addWidget(self.lblModInfo)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnUninstall = QtWidgets.QPushButton(self.groupBox)
        self.btnUninstall.setEnabled(False)
        self.btnUninstall.setObjectName("btnUninstall")
        self.horizontalLayout_2.addWidget(self.btnUninstall)
        self.btnExplore = QtWidgets.QPushButton(self.groupBox)
        self.btnExplore.setEnabled(False)
        self.btnExplore.setObjectName("btnExplore")
        self.horizontalLayout_2.addWidget(self.btnExplore)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(2, 6)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("margin-right: 8px;")
        self.statusbar.setSizeGripEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "BCML: BotW Cemu Mod Loader", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Installed mods:", None, -1))
        self.listWidget.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Drap and drop to change mod load order. Mods at the bottom of the list override mods at the top.", None, -1))
        self.btnInstall.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Install a graphic pack mod", None, -1))
        self.btnInstall.setText(QtWidgets.QApplication.translate("MainWindow", "Install...", None, -1))
        self.btnRemerge.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Perform all merges again", None, -1))
        self.btnRemerge.setText(QtWidgets.QApplication.translate("MainWindow", "Remerge", None, -1))
        self.btnChange.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Apply changes to load order", None, -1))
        self.btnChange.setText(QtWidgets.QApplication.translate("MainWindow", " Apply Sort", None, -1))
        self.btnExport.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Export installed mods as a single mod", None, -1))
        self.btnExport.setText(QtWidgets.QApplication.translate("MainWindow", "Export...", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Mod Info", None, -1))
        self.lblModInfo.setText(QtWidgets.QApplication.translate("MainWindow", "No mod selected", None, -1))
        self.btnUninstall.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Uninstall the selected mod", None, -1))
        self.btnUninstall.setText(QtWidgets.QApplication.translate("MainWindow", "Uninstall", None, -1))
        self.btnExplore.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Open the selected mod in your default file manager", None, -1))
        self.btnExplore.setText(QtWidgets.QApplication.translate("MainWindow", "Explore...", None, -1))

