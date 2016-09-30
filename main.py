from argparse import ArgumentParser
from PIL import Image, ImageFilter

parser=ArgumentParser(description='Convert images to ASCII art')
parser.add_argument('--width', '-w', type=int, default=100, help='width of the output in characters')
parser.add_argument('--font-size', '-f', type=int, default=12, help='size of the font in px')
parser.add_argument('--font-ratio', type=float, default=1.0, help='ratio of the width of the font to the height of the font')
parser.add_argument('--output', '-o', help='output file (defaults to filename.txt)')
parser.add_argument('image', help='input image file')

try:
	img = Image.open("main.jpg")
except:
	print("Unable to load image")

print("Size of image: ")
print(img.format, img.size, img.mode)
