import sys
from mainWindow import *

def runEncrypto(args = None):
	if args is None:
		args = sys.argv[1:]

	mainWindow()



if __name__ == "__main__":
	runEncrypto()