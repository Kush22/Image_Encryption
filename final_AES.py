import sys
from PyQt4 import QtGui, QtCore 
from imgtry import get_pixel_image
from AES import *
import os
import numpy

#adding popups

class Window(QtGui.QMainWindow):	#we can also pass QWidget
	"""docstring for Window"QtGui.QMainWindowf __init__(self, arg):""" 	#we can also inherit form QWidget
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 600, 500)
		self.setWindowTitle("Encrypto - Image Encryption")
		self.setWindowIcon(QtGui.QIcon("home/kush/favicon.ico"))

		#stuff for main menu (for now just file and then Exit)
		quitAction = QtGui.QAction(QtGui.QIcon('favicon.ico'),"&Quit", self)
		quitAction.setShortcut("Ctrl+Q")
		quitAction.setStatusTip('Exit the Encrypto App')
		quitAction.triggered.connect(self.close_application)

		#opening file
		openFileAction = QtGui.QAction(QtGui.QIcon(''), "&Open Image", self)
		openFileAction.setShortcut("Ctrl+O")
		openFileAction.setStatusTip('Open An Image to Encrypt')
		openFileAction.triggered.connect(self.show_openDilog)

		self.statusBar().showMessage('Ready')

		mainMenu = self.menuBar() #We assigned menubar to a variable because we need to attach the items to the fileMenu but we need not attach anything to the statusbar, so No variable has been assigned to it

		#for every menu item we need to write the above 4 lines for quitAction and then attach the action to the menu item
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(quitAction)

		openMenu = mainMenu.addMenu('&Open Image')
		openMenu.addAction(openFileAction)


		self.home()

	def home(self):
		btn = QtGui.QPushButton("Encrypt", self)
		btn.clicked.connect(self.close_application)  #in the connect we pass method, fuction or any such thing
		#QtCore.QCoreApplication.instance().quit -> exits the current state of the application
		
		#we can change the size of button using 'resize()' & to change the position use 'move()'
		#btn.resize(100,100)
		#btn.resize(btn.sizeHint())
		btn.resize(btn.minimumSizeHint())
		btn.move(200,200)
		self.show()

	def close_application(self):
		print("This is the custom button..!!!")
		sys.exit()

	def show_openDilog(self):
		#getOpenFileName returns the path to the selected file
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Select Image', '/home')
		print fname
		if str(fname).lower().endswith(('.png', '.jpg', '.jpeg')):
			img_pixel_values,height,width,channels = get_pixel_image(str(fname)) #The path needs to be sent as a string
			#print img_pixel_values
			
			#new = img_pixel_values.astype(numpy.uint8)   #changing each value to 8-bit (now each pixel value is 24bit) 
			#print new
			key = self.EncryptAES(img_pixel_values,height,width,channels)
			final = self.DecryptAES(height,width,channels,key)
			#print final
			print cmp(img_pixel_values,final)
			print len(final)
			print len(img_pixel_values)
		else:
			print 'Invalid File Format Selected. Select an Image!!!'

	def EncryptAES(self, pixel_array, height, width, channels):
		fptr = open("encrypted_text.txt","w+")
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

	def DecryptAES(self,height, width, channels,key):
		fptr = open("encrypted_text.txt","rw+")
		f = open("decrypted_text.txt","w+")
		original = []
		while 1:
			text = fptr.read(16)
			if(text == ""):
				break
			else:
				decrypted = decryption(text,key)
				for i in range(0,len(decrypted)):
					original.append(ord(decrypted[i]))
		return original




def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()
