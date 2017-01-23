#!/usr/bin/env python3
from argparse import ArgumentParser
from PIL import Image, ImageFilter

parser = ArgumentParser(description='Convert images to ASCII art')
parser.add_argument(
    '--width',
    '-w',
    type=int,
    default=100,
    help='width of the output in characters')
parser.add_argument(
    '--font-ratio',
    '-r',
    type=float,
    default=0.5,
    help='ratio of the width of the font to the height of the font')
parser.add_argument(
    '--output', '-o', help='output file (defaults to filename.txt)')
parser.add_argument('image', help='input image file')
parser.add_argument(
    '--pixel', '-p', help='flag for pixel art mode', action='store_true')
parser.add_argument(
    '--invert',
    '-i',
    help='set foreground color to black and background color to white, only works in ASCII art mode',
    action='store_true')
parser.add_argument(
    '--high',
    '-H',
    help='use more gray levels for more detail',
    action='store_true')
parser.add_argument(
    '--stdout',
    '-s',
    help='output result to stdout, ignore --output',
    action='store_true')
parser.add_argument(
    '--strip-emptylines',
    '-S',
    help='strip useless newlines from beginning and end of the output',
    action='store_true')
args = parser.parse_args()

if not args.stdout:
    if args.output is None:
        args.output = args.image + ".txt"


def foreList(fore):
    return [
        "\033[38;2;", str(fore[0]), ";", str(fore[1]), ";", str(fore[2]), "m"
    ]


def backList(back):
    return [
        "\033[48;2;", str(back[0]), ";", str(back[1]), ";", str(back[2]), "m"
    ]


def colorChar(rgba1, rgba2, b, f):
    upPrint = False
    downPrint = False
    outputList = []
    if rgba1[3] >= 100:
        upPrint = True
    if rgba2[3] >= 100:
        downPrint = True
    if (upPrint and downPrint):
        up = [
            int(rgba1[0] * rgba1[3] / 255), int(rgba1[1] * rgba1[3] / 255),
            int(rgba1[2] * rgba1[3] / 255)
        ]
        down = [
            int(rgba2[0] * rgba2[3] / 255), int(rgba2[1] * rgba2[3] / 255),
            int(rgba2[2] * rgba2[3] / 255)
        ]
        if up == down:
            if b is None:
                b = up
                outputList.extend(backList(b))
            outputList.append(" ")
        else:
            if b is None:
                if f is None:
                    b = up
                    f = down
                    outputList.extend(backList(b))
                    outputList.extend(foreList(f))
                    outputList.append("▄")
                else:
                    if f == down:
                        b = up
                        outputList.extend(backList(b))
                        outputList.append("▄")
                    elif f == up:
                        b = down
                        outputList.extend(backList(b))
                        outputList.append("▀")
                    else:
                        b = up
                        outputList.extend(backList(b))
                        f = down
                        outputList.extend(foreList(f))
                        outputList.append("▄")
            else:
                if b == up:
                    if f is None:
                        f = down
                        outputList.extend(foreList(f))
                        outputList.append("▄")
                    else:
                        if f != down:
                            f = down
                            outputList.extend(foreList(f))
                        outputList.append("▄")
                elif b == down:
                    if f is None:
                        f = up
                        outputList.extend(foreList(f))
                        outputList.append("▀")
                    else:
                        if f != up:
                            f = up
                            outputList.extend(foreList(f))
                        outputList.append("▀")
                else:
                    if f is None:
                        b = up
                        outputList.extend(backList(b))
                        f = down
                        outputList.extend(foreList(f))
                        outputList.append("▄")
                    else:
                        if f == down:
                            b = up
                            outputList.extend(backList(b))
                            outputList.append("▄")
                        elif f == up:
                            b = down
                            outputList.extend(backList(b))
                            outputList.append("▀")
                        else:
                            b = up
                            outputList.extend(backList(b))
                            f = down
                            outputList.extend(foreList(f))
                            outputList.append("▄")

    elif upPrint:
        up = [
            int(rgba1[0] * rgba1[3] / 255), int(rgba1[1] * rgba1[3] / 255),
            int(rgba1[2] * rgba1[3] / 255)
        ]
        if b is not None:
            b = None
            outputList.append("\033[49m")
        if f != up:
            f = up
            outputList.extend(foreList(f))
        outputList.append("▀")
    elif downPrint:
        down = [
            int(rgba1[0] * rgba1[3] / 255), int(rgba1[1] * rgba1[3] / 255),
            int(rgba1[2] * rgba1[3] / 255)
        ]
        if b is not None:
            b = None
            outputList.append("\033[49m")
        if f != down:
            f = down
            outputList.extend(foreList(f))
        outputList.append("▄")
    else:
        if b is not None:
            b = None
            outputList.append("\033[49m")
        else:
            outputList.append(" ")
    output = ''.join(outputList)
    return output, b, f


def asciiChar(intensityTuple):
    if intensityTuple[1] < 100:
        return ' '
    intensity = intensityTuple[0]
    asciiString = ' .:-=+*#%@'
    newIntensity = 9 - int(round(intensity * 10 / 255, 0))
    return asciiString[newIntensity]


def highAsciiChar(intensityTuple):
    if intensityTuple[1] < 100:
        return ' '
    intensity = intensityTuple[0]
    asciiString = ' .\'`^",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
    newIntensity = 69 - int(round(intensity * 70 / 255, 0))
    return asciiString[newIntensity]


try:
    img = Image.open(args.image)
except:
    print("Unable to load image")
    exit()

if args.pixel:
    img = img.convert("RGBA")
    args.font_ratio *= 2
else:
    img = img.convert("LA")
basewidth = args.width
wpercent = float((basewidth / float(img.size[0])))
hsize = int((float(img.size[1]) * wpercent * args.font_ratio))
img = img.resize((basewidth, hsize), Image.LANCZOS)

im = img.load()
width, height = img.size

output = []

if args.pixel:
    b = None
    f = None
    heightPairs = height // 2
    remainder = height % 2
    for i in range(heightPairs - 1):
        for j in range(width):
            newPixel, b, f = colorChar(im[j, i * 2], im[j, i * 2 + 1], b, f)
            output.append(newPixel)
        if b is not None:
            b = None
            output.append('\033[49m')
        output.append('\n')
    i = heightPairs - 1
    for j in range(width):
        newPixel, b, f = colorChar(im[j, i * 2], im[j, i * 2 + 1], b, f)
        output.append(newPixel)
    if remainder != 0:
        if b is not None:
            b = None
            output.append('\033[49m')
        i = height - 1
        for j in range(width):
            newPixel, b, f = colorChar(im[j, i], [0, 0, 0, 0], b, f)
    output.append('\033[0m')

elif args.high:
    for i in range(height):
        if args.invert:
            output.append("\033[30;47m")
        for j in range(width):
            output.append(highAsciiChar(im[j, i]))
        if args.invert:
            output.append("\033[0m")
        output.append('\n')
    del output[-1]
else:
    for i in range(height):
        if args.invert:
            output.append("\033[30;47m")
        for j in range(width):
            output.append(asciiChar(im[j, i]))
        if args.invert:
            output.append("\033[0m")
        output.append('\n')
    del output[-1]

outputString = ''.join(output)

from re import sub
outputString = sub(r' +\n', '\n', outputString)

if args.strip_emptylines:
    if args.pixel:
        outputString = sub(r'^( *(.\[((0)|(49))m)?\n)+', '', outputString)
        outputString = sub(r'\n+ +.\[0m\n?$', '\033[0m', outputString)
    else:
        outputString = sub(r'^( +\n)+', '', outputString)
        outputString = sub(r'\n+ +\n?$', '', outputString)

if args.stdout:
    print(outputString)
else:
    outputFile = open(args.output, "w")
    print(outputString, file=outputFile)
