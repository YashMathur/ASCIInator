#!/usr/bin/env python3
from argparse import ArgumentParser
from PIL import Image, ImageFilter
#import time

parser=ArgumentParser(description='Convert images to ASCII art')
parser.add_argument('--width', '-w', type=int, default=100, help='width of the output in characters')
#parser.add_argument('--font-size', '-f', type=int, default=12, help='size of the font in px')
parser.add_argument('--font-ratio', '-r', type=float, default=0.5, help='ratio of the width of the font to the height of the font')
parser.add_argument('--output', '-o', help='output file (defaults to filename.txt)')
parser.add_argument('image', help='input image file')
args = parser.parse_args()

if args.output is None:
    args.output = args.image + ".txt"

try:
	img = Image.open(args.image)
except:
	print("Unable to load image")
	exit()

basewidth = args.width
wpercent = float((basewidth/float(img.size[0])))
hsize = int((float(img.size[1])*wpercent*args.font_ratio))
img = img.resize((basewidth, hsize))

im = img.load();

width, height = img.size

def colorChar(rgb):
    outputString = "\033[38;2;"+str(rgb[0])+";"+str(rgb[1])+";"+str(rgb[2])+"m█"
    return outputString
output=""
for i in range(0, height-1):
	for j in range(0, width-1):
		output+=colorChar(im[j,i])
	output+='\n'
outputFile = open(args.output,"w")
print(output)
print(output,file = outputFile)
