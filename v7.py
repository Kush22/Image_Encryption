import sys
from PyQt4 import QtGui, QtCore 
from imgtry import get_pixel_image
from AES import encryption
from AES import decryption
import os
import numpy
import base64

#adding popups

class Window(QtGui.QMainWindow):	#we can also pass QWidget
	"""docstring for Window"QtGui.QMainWindowf __init__(self, arg):""" 	#we can also inherit form QWidget

	BLOCK_SIZE = 16
	global key 
	key = os.urandom(BLOCK_SIZE)
	
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
			print img_pixel_values.shape
			
			new = img_pixel_values.astype(numpy.uint8)   #changing each value to 8-bit (now each pixel value is 24bit) 
			print new
			self.DecryptAES(new,height,width,channels)
		else:
			print 'Invalid File Format Selected. Select an Image!!!'

	def EncryptAES(self, pixel_array, height, width, channels):
		fptr = open("encrypted_text.txt","rw+")
		for i in range(0,height):
			for j in range(0,width):
				pixel = ''
				for k in range(0,channels):
					if len(str(pixel_array[i][j][k])) == 1:
						pixel += str(0) + str(0) + str(pixel_array[i][j][k])
					elif len(str(pixel_array[i][j][k])) == 2:
						pixel += str(0) + str(pixel_array[i][j][k])
				#print pixel
				encrypted = encryption(pixel, key)
				#print encrypted
				fptr.write(encrypted)
		fptr.close()

	def DecryptAES(self, pixel_array, height, width, channels):
		fptr = open("encrypted_text.txt","rw+")
		filep = open("decrypted_text.txt", "rw+")
		#filep.write(fptr.read(16))

		print decryption(fptr.read(16), key)
		print "hello"
		'''while True:
			e_text = fptr.read(16)
			if not e_text:
				break
			decrypted = decryption(e_text, key)
			print decrypted
			#filep.write(decrypted)
'''
def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()
