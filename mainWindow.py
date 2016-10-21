#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtGui, QtCore
import sys

import main_window_ui
from encryptWindow import *
from decryptWindow import *
from watermarkWindow import *
from sendDialog import *
from message import *
from email_gmail import *

import socket
import os


from functools import partial

class _MainWindow(QtGui.QMainWindow, main_window_ui.Ui_MainWindow):
	def __init__(self, parent = None):
		super(_MainWindow, self).__init__(parent)
		self.setupUi(self)

		bannerImg = QPixmap('./Images/encrypt_everything_banner.jpg')
		self.imageLabel.setPixmap(bannerImg)
		self.imageLabel.show()

		#Quit Action
		self.actionQuit.triggered.connect(self.close_application)

		#Network-Send Action
		self.actionSend_File.triggered.connect(partial(self.open_fileFn, 3))

		#Network-Receive Action
		self.actionReceive_File.triggered.connect(self.receiveFile)

		#Network-Send RSA Public Key Action
		self.actionSend_RSA_Public_Key.triggered.connect(self.sendRSAkey)

		#Encrypt button functionality
		self.buttonEncrypt_2.clicked.connect(partial(self.open_fileFn, 0))

		#Decrypt button functionality
		self.buttonDecrypt_2.clicked.connect(partial(self.open_fileFn, 1))

		#Watermark button Functionality
		self.buttonWatermark.clicked.connect(partial(self.open_fileFn, 2))

		#disabling the option to resize window size.
		self.setFixedSize(950,400);


	def close_application(self):
		quitChoice = QtGui.QMessageBox.question(self, 'Confirmation',
											"Do you really want to Quit?",
											QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

		if(quitChoice == QtGui.QMessageBox.Yes):
			sys.exit()
		else:
			pass
	
	def sendFile(self,fname):
		#check if to be sent directly or through email/phone
		if fname.endswith('_pass'):

			dlg = SendFileDialog(self)
			if dlg.exec_():
				ip, phone, email = dlg.sendValues()

			userKeyFile = "./EncryptedFiles/" + fname + "/key.kmr"
			f = open(userKeyFile,"rw+")
			userKeyData = f.read()
			
			if phone:
				messagePhoneSend(str(phone), str(userKeyData))
			else:
				messageEmailSend(str(email), str(userKeyData))

			os.makedirs(fname)
			cp_command = "cp -r ./EncryptedFiles/" + fname + "/encrypted_text.kmr " + fname 

		else: 
			#display dialog box to display only the option for IP
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

			
			os.makedirs(fname)
			cp_command = "cp  -r ./EncryptedFiles/" + fname + " ./"

		# zip the encrypted data
		os.system(cp_command)
		zip_it = "zip -r " + fname + ".zip " + fname
		os.system(zip_it)
		os.system('rm -r '+fname)



		s = socket.socket()         # Create a socket object
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		host = ip
		port = 12345                # Reserve a port for your service.

		s.connect((host, port))

		data = fname + ".zip"
		f = open(data,"rb")

		while True:
			chunk = f.read(65536)
			if not chunk:
				break
			s.sendall(chunk)

		os.system("notify-send Encrypto: 'File Sent'")
		os.system('rm -r ' + fname + '.zip')
		s.close() 


	def sendRSAkey(self):
		s = socket.socket()         	# Create a socket object
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		host = ''    			    	# Get local machine name
		port = 12345                	# Reserve a port for your service.
		s.bind((host, port))        	# Bind to the port

		s.listen(5)                 	# Now wait for client connection.
		print 'Server up and running'

		c, addr = s.accept()     		# Establish connection with client.

		#Generate RSA key and send it...
		if os.path.isfile("rsaPrivateKey.txt"):
			f = open("rsaPrivateKey.txt","rw+")
			key = f.read()
			key = RSA.importKey(key)
		else:
			f = open("rsaPrivateKey.txt", "w+")
			random_generator = Random.new().read
			key = RSA.generate( 2048, random_generator) 
			out = key.exportKey()
			f.write(out)

		key = key.publickey()
		key = key.exportKey()
		c.sendall(key)

		os.system("notify-send Encrypto: 'Key Sent'")
		f.close()
		c.close()


	def receiveFile(self):
		s = socket.socket()         # Create a socket object
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		host = ''    			    # Get local machine name
		port = 12345                # Reserve a port for your service.
		s.bind((host, port))        # Bind to the port

		s.listen(5)                 # Now wait for client connection.
		print 'Server up and running'

		c, addr = s.accept()     # Establish connection with client.

		f1 = open("received.zip","wb")
		text = c.recv(65536)
		while (text):
			f1.write(text)
			text = c.recv(65536)
		
		f1.close()

		os.system("notify-send Encrypto: 'File Received'")
		
		if not os.path.exists("ReceivedFiles"):
			os.makedirs("ReceivedFiles")
		os.system("unzip received.zip -d ./ReceivedFiles/")
		os.system("rm -r received.zip")
		c.close()    



	def open_fileFn(self, option):
		#If the the file viewer is opened for Encryption Operation (Option = 0)
		#or watermark operation. In both the cases the selected file should be an image
		if option == 0:
			fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Select Image', '.', "Image Files(*.png *.jpg *.jpeg *.gif *.bmp)"))
			if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
				EncryptDialog(self, fname)
			else:
				pass

		elif option == 1:
			fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Encrypted File', '.', "Encrypto Encrypted Files(*.kmr)"))
			if fname.lower().endswith(('.kmr')):
				DecryptDialog(self, fname)
			else:
				pass

		elif option == 2:
			fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Select Image to Watermark', '.', "Image Files(*.png *.jpg *.jpeg *.gif *.bmp)"))
			if fname.lower().endswith(('.png', '.jpg', '.jpeg', 'gif', '.bmp')):
				WaterMarkDialog(self,fname)
			else:
				pass
		
		elif option == 3:
			fname = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Encrypted File to Send', '.'))
			if fname:
				fname =  os.path.basename(fname)
				self.sendFile(fname)
			else:
				pass


def mainWindow():
	app = QtGui.QApplication(sys.argv)
	GUI = _MainWindow()
	#GUI.resize(900,100)
	GUI.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	mainWindow()