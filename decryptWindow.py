#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Crypto import Random
import Image
import ImageQt
import ImageEnhance
import time
import os.path
import hashlib

from kryptos import * 

class DecryptDialog(QDialog):
	def __init__(self, parent, enFile_path):
	#def __init__(self, enFile_path, parent = None):
		QDialog.__init__(self, parent)
		#super(EncryptDialog, self).__init__(parent)

		self.setGeometry(100,100,600,600)
		self.setWindowTitle('Decryption Window')
		self.enFile_path = enFile_path

		self.image_path = os.path.dirname(self.enFile_path)
		self.image_dir = os.path.basename(self.image_path)
		self.image_name = self.image_dir + ".jpg"

		self.scene = QGraphicsScene()
		self.view = QGraphicsView(self.scene)
		
		#calling the function to display the image
		#0 depicts that the image of lock will be displayed
		self.displayImage(0)

		self.chkboxDES = QCheckBox('DES')
		self.chkboxAES = QCheckBox('AES')
		self.chkboxRSA = QCheckBox('RSA')
		self.spacerItem = QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.labelFName = QLabel('File Selected: '+str(enFile_path))
		self.btnDecrypt = QPushButton("Start Decryption")

		self.keyLengthLabel = QLabel('Enter Key Length: ')
		self.text_key_length = QLineEdit()
		self.keyLabel = QLabel('Enter the Key: ')
		self.text_key = QLineEdit()


		self.chkboxLayout = QHBoxLayout()
		self.chkboxLayout.addWidget(self.chkboxDES)
		self.chkboxLayout.addWidget(self.chkboxAES)
		self.chkboxLayout.addWidget(self.chkboxRSA)

		self.keyLayout = QHBoxLayout()
		self.keyLayout.addWidget(self.keyLengthLabel)
		self.keyLayout.addWidget(self.text_key_length)
		self.keyLayout.addWidget(self.keyLabel)
		self.keyLayout.addWidget(self.text_key)

		layout = QVBoxLayout()
		layout.addWidget(self.view)
		layout.addWidget(self.labelFName)
		layout.addLayout(self.chkboxLayout)

		self.chkboxDES.setEnabled(False)
		self.chkboxAES.setEnabled(False)
		self.chkboxRSA.setEnabled(False)

		rsa = 0

		#individual AES DES directly through channel
		if os.path.isfile(self.image_path + "/key.kmr"):   #individual DES/AES using key directly
			file_path = self.image_path + "/key.kmr"
			self.keyFp = open(file_path, "rw+")
			self.key = self.keyFp.read()
			if len(self.key) == 8:
				self.chkboxDES.toggle()
			else:
				self.chkboxAES.toggle()

		#Combo 
		elif os.path.isfile(self.image_path + "/encrypted_key.kmr"): #combination 
			file_path = self.image_path + "/encrypted_key.kmr"
			f = open(file_path,"rw+")
			algo = f.read(1)
			rsa = 1
			self.chkboxRSA.toggle()
			if algo == "0":			#DES + RSA
				self.chkboxDES.toggle()
			elif algo == "1":		#AES + RSA
				self.chkboxAES.toggle()
			else:					#DES + AES + RSA
				self.chkboxDES.toggle()
				self.chkboxAES.toggle()

		else:   # either individual RSA or password DES/AES
			if self.image_dir.endswith("_pass"):
				# add widget ie 2 textboxes for length and password
				layout.addLayout(self.keyLayout)
				self.KEY_SIZE = self.text_key_length.text()   #extract length in this
				
				self.text_key_length.textChanged.connect(lambda x: self.toggleChkBox())
				self.text_key.editingFinished.connect(self.setKey)
			else:
				rsa = 1
				self.chkboxRSA.toggle()

		if rsa == 1:
			f = open("rsaPrivateKey.txt","rw+")
			self.key = f.read()

		layout.addWidget(self.btnDecrypt)
		
		self.btnDecrypt.clicked.connect(self.startDecrypt)

		self.setLayout(layout)
		self.show()



	def setKey(self):
		self.key = self.text_key.text()			 #extract password in this
		self.key = hashlib.sha256(self.key).digest()

		if self.KEY_SIZE == '8':
			self.key = self.key[24:]
		elif self.KEY_SIZE == '16':
			self.key = self.key[16:]
		elif self.KEY_SIZE == '24':
			self.key = self.key[8:]
		elif self.KEY_SIZE == '32':
			self.key = self.key[:]


	def toggleChkBox(self):
		self.KEY_SIZE = self.text_key_length.text()   #extract length in this

		if self.KEY_SIZE == '8':
			if not self.chkboxDES.isChecked():
				self.chkboxDES.toggle()
			if self.chkboxAES.isChecked():
				self.chkboxAES.toggle()
		else:
			if not self.chkboxAES.isChecked():
				self.chkboxAES.toggle()
			if self.chkboxDES.isChecked():
				self.chkboxDES.toggle()


	def displayImage(self, option):
		if option == 0:
			image = Image.open('./Images/lockDecrypt.jpg')
		if option == 1:
			image = Image.open(self.image_name)

		self.scene.clear()
		width, height = image.size
		
		self.imgQ = ImageQt.ImageQt(image)
		pixMap = QPixmap.fromImage(self.imgQ)
		self.scene.addPixmap(pixMap)
		
		self.view.fitInView(QRectF(0, 0, width, height), Qt.KeepAspectRatio)
		self.scene.update()


	def updateWidget(self):
		self.layout().removeWidget(self.chkboxAES)
		self.chkboxAES.setParent(None)
		self.layout().removeWidget(self.chkboxDES)
		self.chkboxDES.setParent(None)
		self.layout().removeWidget(self.chkboxRSA)
		self.chkboxRSA.setParent(None)
		self.layout().removeWidget(self.btnDecrypt)
		self.btnDecrypt.setParent(None)
		self.layout().removeWidget(self.keyLabel)
		self.keyLabel.setParent(None)
		self.layout().removeWidget(self.text_key)
		self.text_key.setParent(None)
		self.layout().removeWidget(self.keyLengthLabel)
		self.keyLengthLabel.setParent(None)
		self.layout().removeWidget(self.text_key_length)
		self.text_key_length.setParent(None)


		self.layout().removeWidget(self.labelFName)
		self.labelFName.setParent(None)

		self.progressBar = QProgressBar(self)
		self.btnCancel = QPushButton("Cancel")
		self.btnSave = QPushButton("Save")

		self.layout().addWidget(self.progressBar)
		self.chkboxLayout.addWidget(self.btnCancel)
		self.chkboxLayout.addWidget(self.btnSave)

		self.btnCancel.clicked.connect(self.cancelDecrypt)
		self.btnSave.clicked.connect(self.saveFile)


	def saveFile(self):
		print "Saving..."
		os.system("mv ./" + self.image_name + " " + self.image_path)
		os.system("notify-send Encrypto: 'Successfully Saved'")
		self.close()


	def cancelDecrypt(self):
		os.system("rm ./" + self.image_name)		
		os.system("notify-send Encrypto: 'Decryption Cancelled'")
		self.close()


	def startDecrypt(self):
		#check the values of the checkBoxes & then call the functions
		self.updateWidget()
		if self.chkboxDES.isChecked() & self.chkboxAES.isChecked() & self.chkboxRSA.isChecked():
			self.comboDecryption(self.key)
		elif self.chkboxDES.isChecked() & self.chkboxRSA.isChecked():
			self.comboDecryption(self.key)
		elif self.chkboxAES.isChecked() & self.chkboxRSA.isChecked():
			self.comboDecryption(self.key)
		else:
			self.individualDecryption(self.key)
		self.displayImage(1) #3 symbolizes the decrypted image


	def individualDecryption(self,key):
		decrypted, height, width, channels, BLOCK_SIZE = self.Decryption(key)
		self.saveImage(decrypted,height,width,channels)


	def Decryption(self, key):
		fptr = open(self.enFile_path,"rw+")
		decrypted_list = []
		
		if len(key) == 8:
			BLOCK_SIZE = 8
			k = 0
		elif len(key) == 16 or len(key) == 24 or len(key) == 32:
			BLOCK_SIZE = 16
			k = 0
		else:
			key = RSA.importKey(key)
			BLOCK_SIZE = key.size() / 8 
			k = 1

		original = []
		block = 344  # for block of 256 , encoding stores 344 bytes

		height = int(fptr.readline())
		width = int(fptr.readline())
		channels = int(fptr.readline())	

		noOfBlocks = (height*width*channels)/(BLOCK_SIZE) + 1

		for i in range(0,noOfBlocks):
			self.progressBar.setValue((i*100)/(noOfBlocks)+1)
 			QApplication.processEvents() 
			if BLOCK_SIZE == 255:
				text = fptr.read(block)
				k = 1
			else:
				text = fptr.read(BLOCK_SIZE)
				k = 0

			if BLOCK_SIZE == 8:
				decrypted = decryptDES(text,key)

			elif BLOCK_SIZE == 16:
				decrypted = decryptAES(text,key)
			else:
				decrypted = decryptRSA(base64.b64decode(text),key)
			
			decrypted_list += decrypted[k:len(decrypted)]

		return decrypted_list,height,width,channels, BLOCK_SIZE


	def comboDecryption(self,key):
		key_path = self.image_path + "/encrypted_key.kmr"
		f = open(key_path,"rw+")

		algo = f.read(1)
		encrypted_key = f.read()
		key = RSA.importKey(key)
		decrypted_key = decryptRSA(encrypted_key,key)

		if algo == "0" or algo == "1":
			decrypted,height,width,channels, BLOCK_SIZE = self.Decryption(decrypted_key)
			self.saveImage(decrypted,height,width,channels)
		else:
			des_key = decrypted_key[0:8]
			aes_key = decrypted_key[8:len(decrypted_key)]

			decryptedtext, height, width,channels, BLOCK_SIZE = self.Decryption(aes_key)
			values = ""
			values = ''.join(map(str,decryptedtext))

			fptr = open(self.enFile_path,"w+")
			fptr.write(str(height) + "\n" + str(width) + "\n" + str(channels) + "\n")
			fptr.write(values)
			fptr.close()

			decrypted, height, width, channels, BLOCK_SIZE = self.Decryption(des_key)
			self.saveImage(decrypted,height,width,channels)
		

	def saveImage(self,decrypted,height,width,channels):
		original = []

		for j in range(0,height*width*channels):
			original.append(ord(decrypted[j]))

		final = zip(*[iter(original)]*3)

		if channels == 3:
			mode = "RGB"
		elif channels == 1:
			mode = "L"
		elif channels == 4:
			mode = "RGBA"

		image_out = Image.new(mode,(width,height))
		image_out.putdata(final)
		image_out.save(self.image_name, optimize = True)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	image_path = './encrypted_text.kmr'
	widget = DecryptDialog(image_path)
	#widget = EncryptDialog()
	widget.resize(640, 480)
	#widget.show()
	sys.exit(app.exec_())
