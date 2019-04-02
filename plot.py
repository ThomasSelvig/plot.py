# plot a graph
from PIL import Image, ImageDraw, ImageFont
import sys
import ntpath

offset = 25

def getHighest(list):
	# get highest value
	highest = 0
	for i in prm:
		if highest < i:
			highest = i
	return highest

def handleParams(ls):
	global prm
	global highestValue
	global saveFile
	global overlay
	occupiedPrms = 0
		# Parameters:
		#/h val: set highestValue
		#/g formula count: generate (count)amount of (formula)values
		#/help: provides a helpful tutorial
	for index in range(1, len(ls)):
		if "/h" in ls[index]:
			occupiedPrms += 2
			highestValue = int(ls[index + 1])
		elif "/g" in ls[index]:
			occupiedPrms += 3
			nums = ls[index+1].lower().replace("x", "{0}")
			prm = [eval(nums.format(i)) for i in range(int(ls[index+2])+1)]
		elif "/f" in ls[index]:
			occupiedPrms += 2
			saveFile = ls[index + 1]
		elif "/o" in ls[index]:
			occupiedPrms += 1
			overlay = True
		elif "help" in ls[index] or "?" in ls[index]:
			print("Parameters:\n")
			print("\t/h\tset the vertical graph perspective")
			print("\t\t\tExample: /h 20\t")
			print("\t/o\tenable descriptive overlay")
			print("\t\t\tExample: /o")
			print("\t/g\tset a formula and a range")
			print("\t\t\tExample: /g x**2+2 100")
			print("\t/f\tname of image to be saved")
			print("\t\t\tExample: /f image_name.png")
			exit()

	if not "prm" in globals():
		prm = list(map(float, ls[(1+occupiedPrms):]))

# ensure that program is started with a parameter (the first parameter is file name)
if len(sys.argv) >= 2:
	handleParams(sys.argv)
else:
	handleParams(sys.argv + input("Enter Parameters (SPACE Separator): ").split(" "))

# make graph plotting image
img = Image.new("RGB", (1000, 750), color = "rgb(125, 212, 151)")
# enable drawing
draw = ImageDraw.Draw(img)
# enable text
font = ImageFont.truetype("segoeui.ttf", size = 30)

if not "highestValue" in globals():
	highestValue = getHighest(prm)

total = (img.size[0] - offset * 2, img.size[1] - offset * 2)
ratio = (total[0] / float(len(prm)), total[1] / float(highestValue))

# draw top and bottom values of graph
draw.text((offset,offset - 15), str(highestValue), fill = "rgb(0, 111, 85)")
draw.text((offset, total[1] + offset + 5), "0, 0", fill = "rgb(0, 111, 85)")
# draw max horizontal
draw.text((total[0] + offset - 15, total[1] + offset + 5), str(len(prm)), fill = "rgb(0, 111, 85)")

for index in range(len(prm)):
	# if not the last node in list, draw line to next node
	if index < len(prm) - 1:
		draw.line( (index * ratio[0] + offset, (highestValue - prm[index]) * ratio[1] + offset,          (index+1) * ratio[0] + offset, (highestValue - prm[index+1]) * ratio[1] + offset),        fill = 0, width = 2)
	else:
		draw.line( (index * ratio[0] + offset, (highestValue - prm[index]) * ratio[1] + offset,          (index+1) * ratio[0] + offset, (highestValue - prm[index]) * ratio[1] + offset),        fill = 0, width = 2)

	# draw the vertical lines that indicate a new value
	#draw.line((index * ratio[0] + offset, offset,     index * ratio[0] + offset, total[1] + offset),        fill = 0, width = 2)
draw.line( (0 * ratio[0] + offset, offset,    (len(prm)) * ratio[0] + offset, offset), fill = 0, width = 2)
draw.line( (0 * ratio[0] + offset, total[1] + offset,    (len(prm)) * ratio[0] + offset, total[1] + offset), fill = 0, width = 2)

if "overlay" in globals():
	# draw two horizontal lines (1/3 of highestValue between them)
	draw.line( (0 * ratio[0] + offset, offset + ratio[1] * (1/3) * highestValue,    (len(prm)) * ratio[0] + offset, offset + ratio[1] * (1/3) * highestValue), fill = "rgb(179, 43, 43)", width = 2)
	draw.line( (0 * ratio[0] + offset, offset + ratio[1] * (2/3) * highestValue,    (len(prm)) * ratio[0] + offset, offset + ratio[1] * (2/3) * highestValue), fill = "rgb(179, 43, 43)", width = 2)
	# draw info over the two lines
	draw.text((offset,offset - 15 + ratio[1] * (1/3) * highestValue), str(highestValue/3.0*2), fill = "rgb(0, 111, 85)")
	draw.text((offset,offset - 15 + ratio[1] * (2/3) * highestValue), str(highestValue/3.0), fill = "rgb(0, 111, 85)")

img.show()
if "saveFile" in globals():
	if "." in saveFile:
		img.save(saveFile)
	else:
		img.save(saveFile + ".png")
