#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtGui, QtCore
import sys

import main_window_ui
#from encryptWindow import *
from tryEncryptWindow import *

class _MainWindow(QtGui.QMainWindow, main_window_ui.Ui_MainWindow):
	def __init__(self, parent = None):
		super(_MainWindow, self).__init__(parent)
		self.setupUi(self)

		#self.MainWindowImage
		#self.bannerScene = QGraphicsScene()
		#self.MainWindowImage.setScene(self.bannerScene)

		bannerImg = QPixmap('/home/kush/7_Sem/QtDesign/Images/encrypt_everything_banner.jpg')
		self.imageLabel.setPixmap(bannerImg)
		self.imageLabel.show()
		#self.bannerScene.clear()
		#width, height = image.size

		#self.bannerImg = ImageQt.ImageQt(image)
		#pixMap = QPixmap.fromImage(self.bannerImg)
		#self.bannerScene.addPixmap(pixMap)

		#self.MainWindowImage.fitInView(QRectF(0, 0, width, height))
		#self.bannerScene.update()

		#Quit Action
		self.actionQuit.triggered.connect(self.close_application)

		#Encrypt button functionality
		self.buttonEncrypt_2.clicked.connect(self.open_fileFn)


		#this is the reference to the encryptWindow class
		#when a correct image is selected that widget will be executed
		#self.dialogEncrypt = EncryptDialog(self)


	def close_application(self):
		quitChoice = QtGui.QMessageBox.question(self, 'Confirmation',
											"Do you really want to Quit?",
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if(quitChoice == QtGui.QMessageBox.Yes):
			sys.exit()
		else:
			pass

			
	def open_fileFn(self):
		fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Select Image', '.'))
		print fname
		
		if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
			#here create a function that will show a different dialog box with image,
			#checkboxes for the type of encryption and a button for start encryption
			#self.dialogEncrypt.exec_()
			EncryptDialog(self, fname)
		else:
			#Here add a dialog that will say invalid file selected choose a correct one
			print 'Invalid File Format Selected. Select an Image!!!'


def main():
	app = QtGui.QApplication(sys.argv)
	GUI = _MainWindow()
	GUI.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()