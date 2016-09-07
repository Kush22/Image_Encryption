from PIL import Image
import numpy


def get_pixel_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    #print pixel_values
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values,width,height,channels


"""def main():
	image_path = './image.jpg'
	pixel_values = get_pixel_image(image_path)
	print pixel_values.shape
	print pixel_values


main()
"""