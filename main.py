from argparse import ArgumentParser
from PIL import Image, ImageFilter

parser=ArgumentParser(description='Convert images to ASCII art')
parser.add_argument('--width', '-w', type=int, default=100, help='width of the output in characters')
#parser.add_argument('--font-size', '-f', type=int, default=12, help='size of the font in px')
parser.add_argument('--font-ratio', '-r', type=float, default=0.7, help='ratio of the width of the font to the height of the font')
parser.add_argument('--output', '-o', help='output file (defaults to filename.txt)')
parser.add_argument('image', help='input image file')
args = parser.parse_args()

try:
	img = Image.open(args.image).convert('LA')
except:
	print("Unable to load image")
	exit()


# Resizing the image
#print(type(args))
#print(dir(args))
#print(args.font_ratio)
#print('\n')
basewidth = args.width
wpercent = float((basewidth/float(img.size[0])))
hsize = int((float(img.size[1])*wpercent*args.font_ratio))
img = img.resize((basewidth, hsize))


img.save('grayscale.png')
im = img.load();
print("grayscale: ")
print(im[99, 30])
print("Size of image: ")
print(img.format, img.size, img.mode)

width, height = img.size

#for i in range(0, height-1):
#	for j in range(0, width-1):
#		print(ASCIIChar(im[i][j]))
