#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import Image
import ImageQt
import time
from AES import * 

from pixelExtract import get_pixel_image

class EncryptDialog(QDialog):
	def __init__(self, img_path, parent = None):
		QDialog.__init__(self, parent)
		#super(EncryptDialog, self).__init__(parent)

		self.setWindowTitle('Encryption Window')
		self.img_path = img_path
		self.scene = QGraphicsScene()
		self.view = QGraphicsView(self.scene)
		
		#calling the function to display the image
		self.displayImage()

		self.chkboxDES = QCheckBox('DES')
		self.chkboxAES = QCheckBox('AES')
		self.chkboxRSA = QCheckBox('RSA')
		self.btnEncrypt = QPushButton("Start Encryption")

		chkboxLayout = QHBoxLayout()
		chkboxLayout.addWidget(self.chkboxDES)
		chkboxLayout.addWidget(self.chkboxAES)
		chkboxLayout.addWidget(self.chkboxRSA)

		layout = QVBoxLayout()
		layout.addWidget(self.view)
		layout.addLayout(chkboxLayout)
		layout.addWidget(self.btnEncrypt)

		self.setLayout(layout)

		#the startEncrypt() will check the values of the ticked
		#checkboxes and correspondingly will call the appropriate fn
		self.btnEncrypt.clicked.connect(self.startEncrypt)
		self.show()


	def displayImage(self):
		image = Image.open(self.img_path)
		self.scene.clear()
		width, height = image.size
		
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
			key = self.encryptAES(img_pixel_values, height, width, channels)
			print key
		elif self.chkboxRSA.isChecked():
			encryptRSA(self)
		else:
			pass


	def encryptAES(self,pixel_array, height, width, channels):
		fptr = open("encrypted_text.txt","w+")
		fp = open("key.txt","w+")
		#total = height *width * channels - 1
		#i = 0
		text = ''
		BLOCK_SIZE = 16
		key = os.urandom(BLOCK_SIZE)
		for i in range(0, height*width*channels):
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



