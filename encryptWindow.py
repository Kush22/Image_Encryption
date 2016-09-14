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
	#def __init__(self,parent, img_path):
	def __init__(self, img_path, parent = None):
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
			image = Image.open('lock.jpg')

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
				self.Encryption(img_pixel_values, height, width, channels,128)

			print "Encryption Completed"
			final = self.Decryption()

			print cmp(final,img_pixel_values)
			
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
		os.system("rm ./final.*")
		os.system("rm ./key.txt")
		os.system("notify-send Encrypto 'Encryption Cancelled'")
		self.close()

	def saveFile(self):
		print "Saving..."	

	def Encryption(self,pixel_array, height, width, channels,BLOCK_SIZE):
		fptr = open("encrypted_text.txt","w+")
		fp = open("key.txt","w+")
		
		text = ''
		key = os.urandom(BLOCK_SIZE)
		fp.write(key)
		PadBytes = (BLOCK_SIZE-(height*width*channels) % BLOCK_SIZE)%BLOCK_SIZE
		fptr.write(str(height) + "\n" + str(width) + "\n" + str(channels) + "\n" + str(PadBytes) + "\n")

		for i in range(0, height*width*channels):
			#updating the progress Bar
			self.progressBar.setValue((i*100)/(height*width*channels)+1)
			QApplication.processEvents() 

			text += chr(pixel_array[i])
			if (i+1)%BLOCK_SIZE == 0:
				if BLOCK_SIZE == 8:
					encrypted = encryptDES(text,key)
				elif BLOCK_SIZE == 16: 
					encrypted = encryptAES(text,key)
				else:
					encrypted = encryptRSA(text,key)
				fptr.write(encrypted)
				text = ''


	
	def Decryption(self):
		fptr = open("encrypted_text.txt","rw+")
		fp = open("key.txt","rw+")
		f = open("test.txt","w+")

		key = fp.read()
		f.write(key)

		BLOCK_SIZE = len(key)

		original = []

		height = int(fptr.readline())
		width = int(fptr.readline())
		channels = int(fptr.readline())
		padBytes = int(fptr.readline())

		noOfBlocks = (height*width*channels)/BLOCK_SIZE

		for i in range(0,noOfBlocks):
			text = fptr.read(BLOCK_SIZE)
			if BLOCK_SIZE == 8:
				decrypted = decryptDES(text)

			elif BLOCK_SIZE == 16:
				decrypted = decryptAES(text,key)
			else:
				decrypted = decryptRSA(text,key)

			for i in range(0,len(decrypted)):
				original.append(ord(decrypted[i]))

		final = zip(*[iter(original)]*3)
		print len(original)
		print len(final)
		image_out = Image.new("RGB", (640,480),"white")
		image_out.putdata(final)
		image_out.save("final.jpeg", optimize = True)
		return original
	

if __name__ == "__main__":
	app = QApplication(sys.argv)
	image_path = 'image1.jpg'
	widget = EncryptDialog(image_path)
	#widget = EncryptDialog()
	widget.resize(640, 480)
	#widget.show()
	sys.exit(app.exec_())
