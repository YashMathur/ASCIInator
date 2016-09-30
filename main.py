from PIL import Image, ImageFilter

try:
	img = Image.open("main.jpg")
except:
	print "Unable to load image"

print "Size of image: "
print(img.format, img.size, img.mode)
