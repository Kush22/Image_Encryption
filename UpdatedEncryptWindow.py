#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Image
import ImageFilter
import ImageQt
import time

from AES import * 
from pixelExtract import get_pixel_image

class EncryptDialog(QDialog):
	def __init__(self,parent, img_path):
	#def __init__(self, img_path, parent = None):
		QDialog.__init__(self, parent)
		#super(EncryptDialog, self).__init__(parent)

		self.setWindowTitle('Encryption Window')
		self.img_path = img_path
		self.scene = QGraphicsScene()
		self.view = QGraphicsView(self.scene)
		
		#calling the function to display the image
		self.displayImage(0) #0 corresponds to display the original image and 1 to display the blurred image

		self.chkboxDES = QCheckBox('DES')
		self.chkboxAES = QCheckBox('AES')
		self.chkboxRSA = QCheckBox('RSA')
		self.btnEncrypt = QPushButton("Start Encryption")

		self.chkboxLayout = QHBoxLayout()
		self.chkboxLayout.addWidget(self.chkboxDES)
		self.chkboxLayout.addWidget(self.chkboxAES)
		self.chkboxLayout.addWidget(self.chkboxRSA)

		layout = QVBoxLayout()
		layout.addWidget(self.view)
		layout.addLayout(self.chkboxLayout)
		layout.addWidget(self.btnEncrypt)

		self.setLayout(layout)

		#the startEncrypt() will check the values of the ticked
		#checkboxes and correspondingly will call the appropriate fn
		self.btnEncrypt.clicked.connect(self.startEncrypt)
		self.show()


	#0 corresponds to display the original image and 1 to display the blurred image
	def displayImage(self, value):
		image = Image.open(self.img_path)
		if value == 1:
			#lockImage = Image.open('./Images/lock.jpg')
			#image.paste(lockImage, (170, 150), 0)
			image = Image.open('./Images/lock.jpg')

		width, height = image.size
		
		self.scene.clear()
		
		self.imgQ = ImageQt.ImageQt(image)
		pixMap = QPixmap.fromImage(self.imgQ)
		self.scene.addPixmap(pixMap)
		
		self.view.fitInView(QRectF(0, 0, width, height), Qt.KeepAspectRatio)
		self.scene.update()


	def startEncrypt(self):
		#check the values of the checkBoxes & then call the functions
		img_pixel_values, height, width, channels = get_pixel_image(self.img_path)

		if self.chkboxDES.isChecked():
			encryptDES(self)
		elif self.chkboxAES.isChecked():
			self.updateWidget()
			key = self.encryptAES(img_pixel_values, height, width, channels)
			print "Encryption Completed"
			
			#close the encryption window so that a new window showing success and 
			#an option to save the encryted file appears
			
			#self.close()
		elif self.chkboxRSA.isChecked():
			encryptRSA(self)
		else:
			pass


	def updateWidget(self):
		self.layout().removeWidget(self.chkboxAES)
		self.chkboxAES.setParent(None)
		self.layout().removeWidget(self.chkboxDES)
		self.chkboxDES.setParent(None)

		self.layout().removeWidget(self.chkboxRSA)
		self.chkboxRSA.setParent(None)
		self.layout().removeWidget(self.btnEncrypt)
		self.btnEncrypt.setParent(None)


		self.progressBar = QProgressBar(self)
		self.btnCancel = QPushButton("Cancel")
		self.btnSave = QPushButton("Save")


		self.layout().addWidget(self.progressBar)
		self.chkboxLayout.addWidget(self.btnCancel)
		self.chkboxLayout.addWidget(self.btnSave)

		self.btnCancel.clicked.connect(self.cancelEncrypt)
		self.btnSave.clicked.connect(self.saveFile)

		#calling so as to display the encrypted lock image
		self.displayImage(1)
		#self.progressBar.setGeometry(200, 80, 250, 20)
			

	def cancelEncrypt(self):
		os.system("rm ./encrypted_text.txt")
		os.system("notify-send Encrypto 'Encryption Cancelled'")
		self.close()

	def saveFile(self):
		print "Saving..."	

	def encryptAES(self,pixel_array, height, width, channels):
		fptr = open("encrypted_text.txt","w+")
		fp = open("key.txt","w+")
		#total = height *width * channels - 1
		#i = 0
		text = ''
		BLOCK_SIZE = 16
		key = os.urandom(BLOCK_SIZE)
		for i in range(0, height*width*channels):
			#updating the progress Bar
			self.progressBar.setValue(i)
			#QApplication.processEvents() 

			if (i+1)%16 == 0 :
				text += chr(pixel_array[i])
				#print text
				encrypted = encryption(text,key)
				fptr.write(encrypted)
				text = ''
			else:
				text += chr(pixel_array[i])
		return key


if __name__ == "__main__":
	app = QApplication(sys.argv)
	image_path = '/home/kush/Pictures/image.jpg'
	widget = EncryptDialog(image_path)
	#widget = EncryptDialog()
	widget.resize(640, 480)
	#widget.show()
	sys.exit(app.exec_())



