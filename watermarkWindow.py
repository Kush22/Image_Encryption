from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageQt
import os, sys
 
FONT = 'arial.ttf'

class WaterMarkDialog(QDialog):
	def __init__(self, parent, in_file):
		QDialog.__init__(self,parent)

		self.waterImageLabel = QLabel(self)
		self.setWindowTitle('Watermark Window')

		self.waterText, self.ok = QInputDialog.getText(self, 'Text Dialog', 'Enter text to WaterMark:')
		if self.ok:
			self.add_watermark(in_file, str(self.waterText))

		watermarkfile = os.path.basename(os.path.splitext(in_file)[0])  + "_watermark.jpg"
		waterImage = QPixmap(watermarkfile)

	 	self.waterImageLabel.setPixmap(waterImage)
	 	self.waterImageLabel.show()

	 	self.setFixedSize(waterImage.width(), waterImage.height());
	 	self.show()
		

	def add_watermark(self, in_file, text, out_file='watermark.jpg', angle=23, opacity=0.55):
		img = Image.open(in_file).convert('RGB')
		watermark = Image.new('RGBA', img.size, (0,0,0,0))
		size = 10
		n_font = ImageFont.truetype(FONT, size)
		n_width, n_height = n_font.getsize(text)
		
		while n_width+n_height < watermark.size[0]:
			size += 2
			n_font = ImageFont.truetype(FONT, size)
			n_width, n_height = n_font.getsize(text)
		
		draw = ImageDraw.Draw(watermark, 'RGBA')
		draw.text(((watermark.size[0] - n_width) / 2,
					(watermark.size[1] - n_height) / 2),
					 text, font=n_font)
		watermark = watermark.rotate(angle,Image.BICUBIC)
		alpha = watermark.split()[3]

		alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
		watermark.putalpha(alpha)

		out_file = os.path.basename(os.path.splitext(in_file)[0])  + "_watermark.jpg"
		
	 	Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
	 	os.system("notify-send Encrypto 'WaterMark Added'")
	 
	if __name__ == '__main__':
		if len(sys.argv) < 3:
			sys.exit('Usage: %s <input-image> <text> <output-image> ' \
	                 '<angle> <opacity> ' % os.path.basename(sys.argv[0]))
		add_watermark(*sys.argv[1:])