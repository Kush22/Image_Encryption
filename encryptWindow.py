#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Crypto import Random
import Image
import ImageFilter
import ImageQt
import time
import base64
import shutil
import hashlib
import socket
import re

from kryptos import * 
from pixelExtract import get_pixel_image

class EncryptDialog(QDialog):
	def __init__(self,parent, img_path):
	#def __init__(self, img_path, parent = None):
		QDialog.__init__(self, parent)

		if not os.path.exists("EncryptedFiles"):
			os.makedirs("EncryptedFiles")

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
		self.labelRSA = QLabel("RSA Key Size : 256 bytes")

		self.labelDES.setEnabled(False)
		self.comboBoxAES.setEnabled(False)
		self.labelRSA.setEnabled(False)

		#self.comboBoxAES.addItem("AES Key Size")
		self.comboBoxAES.addItem("16")
		self.comboBoxAES.addItem("24")
		self.comboBoxAES.addItem("32")

		#Radio button to select for choice of sending the secret key
		self.radio_key = QRadioButton("Enter the Key")
		self.radio_key.setChecked(True)
		self.radio_generate = QRadioButton("Generate Key Automatically")
		self.text_key = QLineEdit()
		
		self.chkboxLayout = QGridLayout()
		self.chkboxLayout.addWidget(self.chkboxDES, 0, 0)
		self.chkboxLayout.addWidget(self.chkboxAES, 0, 1)
		self.chkboxLayout.addWidget(self.chkboxRSA, 0, 2)
		self.chkboxLayout.addWidget(self.labelDES, 1, 0)
		self.chkboxLayout.addWidget(self.comboBoxAES, 1, 1)
		self.chkboxLayout.addWidget(self.labelRSA, 1, 2)
		
		self.chkboxDES.stateChanged.connect(lambda x:self.chkboxDESStateChange())
		self.chkboxAES.stateChanged.connect(lambda x:self.chkboxAESStateChange())
		self.chkboxRSA.stateChanged.connect(lambda x:self.chkboxRSAStateChange())
		
		layout = QVBoxLayout()
		layout.addWidget(self.view)
		layout.addLayout(self.chkboxLayout)
		layout.addWidget(self.btnEncrypt)

		self.setLayout(layout)

		self.btnEncrypt.clicked.connect(lambda x: self.startEncryptFunction())
		self.show()


	def startEncryptFunction(self):
		if (self.chkboxDES.isChecked() and self.chkboxAES.isChecked() and not self.chkboxRSA.isChecked()):
			os.system("notify-send Encrypto: 'Invalid Combination	'")
			pass
		elif (not self.chkboxDES.isChecked() and not self.chkboxAES.isChecked() and not self.chkboxRSA.isChecked()):
			pass
		else:
			self.startEncrypt()


	def chkboxDESStateChange(self):
		if self.chkboxDES.isChecked():
			self.labelDES.setEnabled(True)
			if(not self.chkboxAES.isChecked() and not self.chkboxRSA.isChecked()):
				self.showRadioButton()
				self.showKeyText()
		else:
			self.labelDES.setEnabled(False)
			if(not self.chkboxAES.isChecked()):
				self.removeRadioButton()


	def chkboxAESStateChange(self):
		if self.chkboxAES.isChecked():
			self.comboBoxAES.setEnabled(True)
			if(not self.chkboxDES.isChecked() and not self.chkboxRSA.isChecked()):
				self.showRadioButton()
				self.showKeyText()
		else:
			self.comboBoxAES.setEnabled(False)
			if(not self.chkboxDES.isChecked()):
				self.removeRadioButton()
	

	def chkboxRSAStateChange(self):
		if self.chkboxRSA.isChecked():
			self.labelRSA.setEnabled(True)
			if(self.chkboxDES.isChecked() or self.chkboxAES.isChecked()):
				self.removeRadioButton()
		else:
			self.labelRSA.setEnabled(False)
			if(self.chkboxDES.isChecked() or self.chkboxAES.isChecked()):
				self.showRadioButton()
				self.showKeyText()


	def showRadioButton(self):
		self.chkboxLayout.addWidget(self.radio_key, 2, 0)
		self.chkboxLayout.addWidget(self.radio_generate, 2, 1)
		self.radio_key.toggled.connect(lambda x:self.showKeyText())
		self.radio_generate.toggled.connect(lambda x:self.showKeyText())


	def removeRadioButton(self):
		self.layout().removeWidget(self.radio_key)
		self.radio_key.setParent(None)
		self.layout().removeWidget(self.radio_generate)
		self.radio_generate.setParent(None)
		self.layout().removeWidget(self.text_key)
		self.text_key.setParent(None)
		self.text_key.setText("")


	def showKeyText(self):
		if(self.radio_key.isChecked()):
			self.chkboxLayout.addWidget(self.text_key,3,0,1,3)

		if(self.radio_generate.isChecked()):
			self.layout().removeWidget(self.text_key)
			self.text_key.setParent(None)


	#0 corresponds to display the original image and 1 to display the blurred image & 2 corresponds to the final lock image
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
		
		self.view.fitInView(QRectF(0, 0, width, height), Qt.KeepAspectRatio)
		self.scene.update()


	def updateWidget(self):
		self.removeRadioButton()
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
		self.layout().removeWidget(self.labelRSA)
		self.labelRSA.setParent(None)

		self.progressBar = QProgressBar(self)
		self.btnCancel = QPushButton("Cancel")
		self.btnSave = QPushButton("Save")

		self.layout().addWidget(self.progressBar)
		self.chkboxLayout.addWidget(self.btnCancel)
		self.chkboxLayout.addWidget(self.btnSave)

		self.btnCancel.clicked.connect(self.cancelEncrypt)
		self.btnSave.clicked.connect(self.saveFile)
			

	def cancelEncrypt(self):
		files = os.listdir('.')
		res =list(filter(lambda x:x.endswith('.kmr'),files))
		for i in range(0,len(res)):
			kmr_file = "rm " + str(res[i]) 
			os.system(kmr_file)

		os.system("notify-send Encrypto: 'Encryption Cancelled'")
		self.close()


	def saveFile(self):
		if self.userKeyFlag == 1:
			var = "pass"
		else:
			var = "key"

		i = 1
		dir_name = os.path.basename(os.path.splitext(self.img_path)[0]) 
		name = dir_name + "_" + var

		while(1):
			path1 = "./EncryptedFiles/" + name
			if not os.path.exists(path1):
				os.makedirs(name)
				break
			else:
				name = dir_name + "_" + str(i) + "_" + var
				i = i + 1


		if self.userKeyFlag == 1:
			f = open("key.kmr","a")
			f.write(name)
			f.close()

		#moving all .kmr files in directory 
		files = os.listdir('.')
		res =list(filter(lambda x:x.endswith('.kmr'),files))
		for i in range(0,len(res)):
			src = res[i]
			dest = "./" + name + "/"+ res[i] 
			shutil.move(src, dest)

		#move file to Encrypted files directory
		mv_command = "mv ./" + name + " ./EncryptedFiles/"
		os.system(mv_command)

		os.system("notify-send Encrypto: 'Successfully Saved'")
		self.close()	


	def startEncrypt(self):
		#check the values of the checkBoxes & then call the functions
		img_pixel_values,width, height,channels = get_pixel_image(self.img_path)

		#checking if the user choosed the option of entering the key
		self.userKey = self.text_key.text()

		if self.userKey:
			self.userKeyFlag = 1
		else:
			self.userKeyFlag = 0

		self.displayImage(1)

		if self.chkboxDES.isChecked() | self.chkboxAES.isChecked() | self.chkboxRSA.isChecked():
			self.updateWidget()   #if any checkbox is marked then update widget

			if self.chkboxDES.isChecked() & self.chkboxAES.isChecked() & self.chkboxRSA.isChecked():
				self.comboEncryption(img_pixel_values,height,width,channels,int(self.comboBoxAES.currentText()),256,"both")
	
			elif self.chkboxDES.isChecked() & self.chkboxRSA.isChecked():
				self.comboEncryption(img_pixel_values,height,width,channels,8,256,"des")

			elif self.chkboxAES.isChecked() & self.chkboxRSA.isChecked():
				self.comboEncryption(img_pixel_values,height,width,channels,int(self.comboBoxAES.currentText()),256,"aes")

			elif self.chkboxDES.isChecked():     #only DES
				self.Encryption(img_pixel_values, height, width, channels,8)

			elif self.chkboxAES.isChecked():     #only AES
				self.Encryption(img_pixel_values, height, width, channels,int(self.comboBoxAES.currentText()))
			
			elif self.chkboxRSA.isChecked():	 #only RSA							
				self.Encryption(img_pixel_values, height, width, channels,256)

			self.displayImage(2)
			
		else:
			pass

	def getRSAkey(self):
		s = socket.socket()         							# Create a socket object
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		port = 12345                							# Reserve a port for your service.


		ipValid = False
			
		while not ipValid:
			ip , ok = QInputDialog.getText(self, 'Enter IP Dialog', 'Enter IP of the Server:')
			ipCheck = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)

			if not ok:
				break

			if ipCheck:
				ipValid = True
			else:
				os.system("notify-send Encrypto: 'Invalid IP. Enter A correct one'")
											  

		s.connect((ip, port))

		f = open("rsaPublicKey.txt","w+")
		key = s.recv(65536)
		f.write(key)
		f.close()
		s.close()


	def Encryption(self,pixel_array, height, width, channels,KEY_SIZE):
		#Two files are created : one stores encrypted data and key in other
 		fptr = open("encrypted_text.kmr","w+")
 		
 		text = ''
 		if KEY_SIZE == 256:   #RSA
			self.getRSAkey()
			f1 = open("rsaPublicKey.txt","rw+")
			key = f1.read()
			key = RSA.importKey(key)
			os.system("rm -r rsaPublicKey.txt")
			BLOCK_SIZE = KEY_SIZE -1
		else:
			f = open("key.kmr","w+")
			if self.userKeyFlag:
				#here use the SHA algorithm to make the key of appropriate size
				key = hashlib.sha256(self.userKey).digest()
			else:		
				key = os.urandom(KEY_SIZE)   
			
			if KEY_SIZE == 8 :   #DES
				if self.userKeyFlag:
					key = key[24:]	#extracting the last 8 bytes
				BLOCK_SIZE = 8
				#here too extract the required length from the key if the flag == true
			else:
				if self.userKeyFlag:
					if KEY_SIZE == 16:
						key = key[16:]	#extracting the last 16 bytes
					elif KEY_SIZE == 24:
						key = key[8:]	#extracting last 24 bytes
					else:
						key = key[:]	#in case KEYSIZE = 32 whole key is needed
				BLOCK_SIZE = 16	 #AES
			if self.userKeyFlag:
				f.write(str(KEY_SIZE) + " : " + self.userKey + " : ")
			else:
				f.write(key)


 		fptr.write(str(height) + "\n" + str(width) + "\n" + str(channels) + "\n")
 
 		for i in range(0, height*width*channels):
 			#updating the progress Bar
 			self.progressBar.setValue((i*100)/(height*width*channels)+1)
 			QApplication.processEvents() 

 			if text == "" and (BLOCK_SIZE + 1) % KEY_SIZE == 0:
 				text += chr(48)

 			if isinstance(pixel_array[i], int):
 				text += chr(pixel_array[i])
 			else:
 				text += pixel_array[i]

 			if (i+1) % (BLOCK_SIZE) == 0 or (i+1) == (height*width*channels):
				if BLOCK_SIZE == 8:
					encrypted = encryptDES(text,key)
					fptr.write(encrypted)

				elif BLOCK_SIZE == 16: 
					encrypted = encryptAES(text,key)
					fptr.write(encrypted)

				else:
					encrypted = encryptRSA(text,key)
					while len(encrypted) < KEY_SIZE:
						encrypted = "\x00" + encrypted
					fptr.write(base64.b64encode(encrypted))
				text = ''


	def comboEncryption(self,pixel_array, height, width, channels,SKEY_SIZE,AKEY_SIZE,algo):
		fptr= open("encrypted_key.kmr","w+")
		if algo == "des":
			self.Encryption(pixel_array, height, width, channels, 8)
			fptr.write("0")    #0 means DES
		elif algo == "aes":
			self.Encryption(pixel_array, height, width, channels, SKEY_SIZE)
			fptr.write("1")    #1 means AES
		else:
			self.Encryption(pixel_array, height, width, channels, 8)
			fptr.write("2")	   #2 means both AES and DES
			
			f = open("key.kmr","rw+")
			des_key = f.read()
			f.close()

			#store new data in list i.e. data encrypted by DES
			pixel_array = []
			f = open("encrypted_text.kmr","rw+")
			height = int(f.readline())
			width = int(f.readline())
			channels = int(f.readline())

			pixel_array = f.read()
			f.close()

			# call for AES
			self.Encryption(pixel_array, height, width, channels, SKEY_SIZE)

			f1 = open("key.kmr","rw+")
			aes_key = f1.read() 
			f1.seek(0,0)
			f1.write(des_key + aes_key)
			f1.close()


		f = open("key.kmr","rw+")
		key = f.read()  #data to be encrypted
		f.close()
		os.system("rm key.kmr")

		self.getRSAkey()
		f1 = open("rsaPublicKey.txt","rw+")
		RSA_key = f1.read()
		RSA_key = RSA.importKey(RSA_key)
		os.system("rm -r rsaPublicKey.txt")

		encrypted = encryptRSA(key, RSA_key)
		fptr.write(encrypted)
		
if __name__ == "__main__":
	app = QApplication(sys.argv)
	image_path = './Images/image.jpg'
	widget = EncryptDialog(image_path)
	#widget = EncryptDialog()
	widget.resize(640, 480)
	#widget.show()
	sys.exit(app.exec_())