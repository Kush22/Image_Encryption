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

from kryptos import * 
from pixelExtract import get_pixel_image

class EncryptDialog(QDialog):
	def __init__(self,parent, img_path):
	#def __init__(self, img_path, parent = None):
		QDialog.__init__(self, parent)
		#super(EncryptDialog, self).__init__(parent)

		self.setGeometry(100,100,600,600)
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
		self.labelDES = QLabel("DES Key Size : 8 bytes")
		self.comboBoxAES = QComboBox(self)
		self.comboBoxRSA = QComboBox(self)

		self.comboBoxAES.setEnabled(False)
		self.comboBoxRSA.setEnabled(False)


		self.comboBoxAES.addItem("AES Key Size")
		self.comboBoxAES.addItem("16")
		self.comboBoxAES.addItem("24")
		self.comboBoxAES.addItem("32")

		self.comboBoxRSA.addItem("RSA Key Size")
		self.comboBoxRSA.addItem("128")
		self.comboBoxRSA.addItem("256")
		self.comboBoxRSA.addItem("512")

		#self.chkboxLayout = QHBoxLayout()
		self.chkboxLayout = QGridLayout()
		self.chkboxLayout.addWidget(self.chkboxDES, 0, 0)
		self.chkboxLayout.addWidget(self.chkboxAES, 0, 1)
		self.chkboxLayout.addWidget(self.chkboxRSA, 0, 2)
		self.chkboxLayout.addWidget(self.labelDES, 1, 0)
		self.chkboxLayout.addWidget(self.comboBoxAES, 1, 1)
		self.chkboxLayout.addWidget(self.comboBoxRSA, 1, 2)

		self.chkboxAES.stateChanged.connect(lambda x:self.comboBoxAES.setEnabled(True) if self.chkboxAES.isChecked() else self.comboBoxAES.setEnabled(False))
		self.chkboxRSA.stateChanged.connect(lambda x:self.comboBoxRSA.setEnabled(True) if self.chkboxRSA.isChecked() else self.comboBoxRSA.setEnabled(False))
		
		#self.overlayLabel1 = QLabel("Encrypting.", self)
		'''self.font = QFont()
		self.font.setPixelSize(10)
		self.font.setBold(false)
		self.font.setFamily("Calibri")'''
		
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
			image = Image.open('./Images/encrypting.jpg')
		if value == 2:
			image = Image.open('./Images/lock.jpg')

		width, height = image.size
		
		self.scene.clear()
		

		self.imgQ = ImageQt.ImageQt(image)
		pixMap = QPixmap.fromImage(self.imgQ)
		self.scene.addPixmap(pixMap)

		'''if value == 1:
			self.overlayLabel1 = QGraphicsTextItem()
			self.overlayLabel1.setHtml("<h1 align=\"center\">Encrypting.</h1>");
			self.overlayLabel1.setPos(QPointF(200,100))
			self.scene.addItem(self.overlayLabel1)
			#self.scene.addText(100, 50, self.font, "Encryption")'''
		
		self.view.fitInView(QRectF(0, 0, width, height), Qt.KeepAspectRatio)
		self.scene.update()


	def startEncrypt(self):
		#check the values of the checkBoxes & then call the functions
		img_pixel_values, height, width, channels = get_pixel_image(self.img_path)

		'''screenShape = self.frameGeometry()
		print screenShape.width()
		print screenShape.height()
		self.overlayLabel1 = QGraphicsTextItem()
		self.overlayLabel1.setHtml("<h1><font color = \"cyan\"> Encrypting. . .</font></h1>")
		self.overlayLabel1.setPos(QPointF(100,20))
		self.scene.addItem(self.overlayLabel1)'''
		self.displayImage(1)

		if self.chkboxDES.isChecked() | self.chkboxAES.isChecked() | self.chkboxRSA.isChecked():
			self.updateWidget()   #if any checkbox is marked then update widget

			if self.chkboxDES.isChecked() & self.chkboxAES.isChecked() & self.chkboxRSA.isChecked():
				self.Combination()
			elif self.chkboxDES.isChecked() & self.chkboxAES.isChecked():
				self.Combination()
			elif self.chkboxDES.isChecked() & self.chkboxRSA.isChecked():
				self.Combination()
			elif self.chkboxAES.isChecked() & self.chkboxRSA.isChecked():
				self.Combination()

			elif self.chkboxDES.isChecked():     #only DES
				self.Encryption(img_pixel_values, height, width, channels,8)

			elif self.chkboxAES.isChecked():     #only AES
				self.Encryption(img_pixel_values, height, width, channels,16)

			elif self.chkboxRSA.isChecked():	 #only RSA			
			#implement a combo box with the values 1024 bits, 2048 bits, 4096 bits				
				self.Encryption(img_pixel_values, height, width, channels,128)

			self.displayImage(2)
			print "Encryption Completed"
			
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


		self.layout().removeWidget(self.labelDES)
		self.labelDES.setParent(None)
		self.layout().removeWidget(self.comboBoxAES)
		self.comboBoxAES.setParent(None)
		self.layout().removeWidget(self.comboBoxRSA)
		self.comboBoxRSA.setParent(None)

		self.progressBar = QProgressBar(self)
		self.btnCancel = QPushButton("Cancel")
		self.btnSave = QPushButton("Save")

		#self.overlayLabel1 = QLabel("Encrypting.", self)
		#self.overlayLabel2 = QLabel("Encrypting..", self)
		#self.overlayLabel3 = QLabel("Encrypting...", self)

		self.layout().addWidget(self.progressBar)
		self.chkboxLayout.addWidget(self.btnCancel)
		self.chkboxLayout.addWidget(self.btnSave)

		self.btnCancel.clicked.connect(self.cancelEncrypt)
		self.btnSave.clicked.connect(self.saveFile)

		#calling so as to display the encrypted lock image
		
		#self.progressBar.setGeometry(200, 80, 250, 20)
			

	def cancelEncrypt(self):
		os.system("rm ./encrypted_text.txt")
		os.system("notify-send Encrypto 'Encryption Cancelled'")
		sys.exit()

	def saveFile(self):
		print "Saving..."	

	def Encryption(self, pixel_array, height, width, channels, BLOCK_SIZE):
		fptr = open("encrypted_text.txt","w+")
		fp = open("key.txt","w+")
		text = ''
		
		key = os.urandom(BLOCK_SIZE)
		fp.write(key + '\n')
		for i in range(0, height*width*channels):
			#updating the progress Bar
			self.progressBar.setValue((i*100)/(height * width * channels)+1)
			QApplication.processEvents() 

			text += chr(pixel_array[i])
			if (i+1)%BLOCK_SIZE == 0:
				
				if BLOCK_SIZE == 8:
					encrypted = encryptDES(text, key)
				
				elif BLOCK_SIZE == 16: 
					encrypted = encryptAES(text, key)
				
				else:
					encrypted = encryptRSA(text, key)
				fptr.write(encrypted)
				text = ''
			
			elif (i+1) == (height * width * channels):        #no of padding bytes required
				fp.write(str(BLOCK_SIZE - (height * width * channels % BLOCK_SIZE)))


	def Decryption(self,height, width, channels,BLOCK_SIZE):
		fptr = open("encrypted_text.txt","rw+")
		fp = open("key.txt","r+")
		lines = fp.readlines()
		key = lines[0]   #first line is key
		padding = lines[1]   #second line is no of bytes padded
		original = []   #stores the final decrypted array
		while 1:
			text = fptr.read(BLOCK_SIZE)
			if(text == ""):
				break
			else:
				decrypted = decryption(text,key)
				for i in range(0,len(decrypted)):
					original.append(ord(decrypted[i]))
		return originals


if __name__ == "__main__":
	app = QApplication(sys.argv)
	image_path = './Images/image.jpg'
	widget = EncryptDialog(image_path)
	#widget = EncryptDialog()
	widget.resize(640, 480)
	#widget.show()
	sys.exit(app.exec_())
