from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys, re
 
class SendFileDialog(QDialog):
	#def __init__(self, parent):
	def __init__(self, parent = None):
		QDialog.__init__(self,parent)
		self.correct = False
		self.ip = ""
		self.email = ""
		self.phone = ""
		
		self.setGeometry(400,175,450,175)
		self.setWindowTitle('Send Image Dialog')

		self.ipLabel = QLabel()
		self.ipLabel.setText("Enter IP of the server")
		self.textIpReceiver = QLineEdit()
		self.errorLabel = QLabel()
		#self.textIpReceiver.setInputMask('000.000.000.000')

		self.radioBtnMobile = QRadioButton('Send Key through Phone')
		self.radioBtnEmail = QRadioButton('Send Key through E-mail')
		self.textPhone = QLineEdit()
		self.textPhone.setInputMask('9999999999')
		self.textEmail = QLineEdit()
		self.sendBtn = QPushButton("Send")

		#self.spacerItem = QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		
		layout = QVBoxLayout()

		self.ipLayout = QHBoxLayout();
		self.ipLayout.addWidget(self.ipLabel)
		self.ipLayout.addWidget(self.textIpReceiver)

		self.radioBtnLayout = QGridLayout()
		self.radioBtnLayout.addWidget(self.radioBtnMobile, 0, 0)
		self.radioBtnLayout.addWidget(self.radioBtnEmail, 0, 1)

		layout.addLayout(self.ipLayout)
		layout.addLayout(self.radioBtnLayout)
		layout.addWidget(self.sendBtn)
		self.setLayout(layout)

		self.radioBtnMobile.toggled.connect(self.dispEditBox)
		self.radioBtnEmail.toggled.connect(self.dispEditBox)

		self.sendBtn.clicked.connect(lambda x:self.sendBtnCheck())

	 	self.show()

	def sendValues(self):
		if self.correct:
			return self.ip, self.phone, self.email
		
	def dispEditBox(self):
		if self.radioBtnMobile.isChecked():
			self.layout().removeWidget(self.textEmail)
			self.textEmail.setParent(None)
			self.radioBtnLayout.addWidget(self.textPhone,1,0,1,2)
		if self.radioBtnEmail.isChecked():
			self.layout().removeWidget(self.textPhone)
			self.textPhone.setParent(None)
			self.radioBtnLayout.addWidget(self.textEmail,1,0,1,2)

	def sendBtnCheck(self):
		self.ip = self.textIpReceiver.text()
		self.email = self.textEmail.text()
		self.phone = self.textPhone.text()

		self.ipCheck = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", self.ip)
		self.emailCheck = re.match(r"[^@]+@[^@]+\.[^@]+$", self.email)
		self.phoneCheck = re.match(r"^\d\d\d\d\d\d\d\d\d\d$", self.phone)

		self.layout().addWidget(self.errorLabel)
		
		if self.ipCheck:
			if self.radioBtnEmail.isChecked():
				if self.emailCheck:
					self.correct = True
					self.accept()
					#return (self.ip, self.phone, self.email)
				else:
					self.errorLabel.setText("Email Invalid")
			elif self.radioBtnMobile.isChecked():
				if self.phoneCheck:
					self.correct = True
					self.accept()
					#return  (self.ip, self.phone, self.email)
					#call the neccessary function
				else:
					self.errorLabel.setText("Mobile Number Invalid")
		else:
			self.errorLabel.setText("IP Address Invalid")






	 
if __name__ == "__main__":
	app = QApplication(sys.argv)
	widget = SendFileDialog()
	#widget = EncryptDialog()
	#widget.resize(640, 480)
	#widget.show()
	sys.exit(app.exec_())
