# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main_Window.ui'
#
# Created: Sat Sep 10 13:19:51 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(465, 417)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.imageLabel = QtGui.QLabel(self.centralwidget)
        self.imageLabel.setObjectName(_fromUtf8("imageLabel"))
        self.verticalLayout_2.addWidget(self.imageLabel)
        spacerItem = QtGui.QSpacerItem(17, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        spacerItem1 = QtGui.QSpacerItem(442, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(442, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        spacerItem3 = QtGui.QSpacerItem(17, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(78, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.labelOption = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.labelOption.setFont(font)
        self.labelOption.setFocusPolicy(QtCore.Qt.NoFocus)
        self.labelOption.setObjectName(_fromUtf8("labelOption"))
        self.horizontalLayout_4.addWidget(self.labelOption)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem7 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelEncrpyt = QtGui.QLabel(self.centralwidget)
        self.labelEncrpyt.setObjectName(_fromUtf8("labelEncrpyt"))
        self.horizontalLayout.addWidget(self.labelEncrpyt)
        self.buttonEncrypt_2 = QtGui.QPushButton(self.centralwidget)
        self.buttonEncrypt_2.setFocusPolicy(QtCore.Qt.TabFocus)
        self.buttonEncrypt_2.setObjectName(_fromUtf8("buttonEncrypt_2"))
        self.horizontalLayout.addWidget(self.buttonEncrypt_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem8 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem8)
        spacerItem9 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem9)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelDecrypt = QtGui.QLabel(self.centralwidget)
        self.labelDecrypt.setObjectName(_fromUtf8("labelDecrypt"))
        self.horizontalLayout_2.addWidget(self.labelDecrypt)
        self.buttonDecrypt_2 = QtGui.QPushButton(self.centralwidget)
        self.buttonDecrypt_2.setObjectName(_fromUtf8("buttonDecrypt_2"))
        self.horizontalLayout_2.addWidget(self.buttonDecrypt_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem10 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        spacerItem11 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem11)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelWatermark = QtGui.QLabel(self.centralwidget)
        self.labelWatermark.setObjectName(_fromUtf8("labelWatermark"))
        self.horizontalLayout_3.addWidget(self.labelWatermark)
        self.buttonWatermark = QtGui.QPushButton(self.centralwidget)
        self.buttonWatermark.setObjectName(_fromUtf8("buttonWatermark"))
        self.horizontalLayout_3.addWidget(self.buttonWatermark)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 465, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFilr = QtGui.QMenu(self.menubar)
        self.menuFilr.setObjectName(_fromUtf8("menuFilr"))
        MainWindow.setMenuBar(self.menubar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setIconVisibleInMenu(False)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFilr.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFilr.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Encrypto", None))
        self.imageLabel.setText(_translate("MainWindow", "TextLabel", None))
        self.labelOption.setText(_translate("MainWindow", "Select the Option", None))
        self.labelEncrpyt.setText(_translate("MainWindow", "1. Encrypt Image", None))
        self.buttonEncrypt_2.setText(_translate("MainWindow", "Encrypt", None))
        self.labelDecrypt.setText(_translate("MainWindow", "2. Decrypt Image", None))
        self.buttonDecrypt_2.setText(_translate("MainWindow", "Decrypt", None))
        self.labelWatermark.setText(_translate("MainWindow", "3.Add Watermark", None))
        self.buttonWatermark.setText(_translate("MainWindow", "Watermark", None))
        self.menuFilr.setTitle(_translate("MainWindow", "File", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))

