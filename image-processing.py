from PIL import Image
import multiprocessing as mp
import threading
import time

img = Image.open('house.png')
newImg = img.copy()
currentPix = img.load() # get the pixels
newPix = newImg.load() # get the pixels


"""To add a new function:
	give it the same 4 arguments as seen in mirrorRightToLeft
	width is the width of the image
	height is the last horizontal line the function is tasked with dealing with
	step is how many lines the function is tasked with dealing with
	que is the queue... honestly we might be able to remove this unless we need per-thread timing
	
	The first scan line you deal with will be height-step
	The last will just be height.
	
	After you get your function written, add it to  the options variable in main.
"""
def mirrorRightToLeft(width, height, step, que):
	global newImg
	global currentPix
	global newPix
	# Record time for function
	ftime = time.time()
	# make image symmetric about a vertical axis
	for x in range(int(width/2)):
		for y in range(height-step,height):
			try:
				newPix[x,y] = currentPix[width-1-x, y]
			except IndexError:
				print("INDEX ERROR AT:", (x,y))
				exit()

def mirrorLeftToRight(width, height, step, que):
	global newImg
	global currentPix
	global newPix
	# Record time for function
	ftime = time.time()
	# make image symmetric about a vertical axis
	for x in range(int(width/2)+1, width):
		for y in range(height-step,height):
			try:
				newPix[x,y] = currentPix[width-1-x, y]
			except IndexError:
				print("INDEX ERROR AT:", (x,y))
				exit()	

def lapalacian(width, height, step, que):
	#discrete laplace
	global newImg
	global currentPix
	global newPix
	
	kernel = ((0,1,0),(1,-4,1),(0,1,0))
	for x in range(width):
		for y in range(height):
			r = 0
			g = 0
			b = 0
			for xb in range(0,3):
				for yb in range(0,3):
					if kernel[xb][yb] != 0:
						pixel = getPixelWithOverlap(x+xb-1, y+yb-1, width, height)
						r+= pixel[0] * kernel[xb][yb]
						g+= pixel[1] * kernel[xb][yb]
						b+= pixel[2] * kernel[xb][yb]
			r = r
			b = b
			g = g
			newPix[x,y] = ( r, g, b)
					
	
def getPixelWithOverlap(x,y, width, height):
	global currentPix
	
	if x < 0:
		x = width + x
	elif x>=width:
		x = x-width
	if y<0:
		y = height + y
	elif y>=height:
		y = y-height
	return currentPix[x,y]

def main():
	global img
	global newImg
	global currentPix
	global newPix
	que = mp.Queue()

	width, height = img.size

	print "You have " + str(mp.cpu_count()) + " logical cores." # get the number of cores
	imageNumber = 0
	#define function options
	options ={
		0: mirrorRightToLeft,
		1: mirrorLeftToRight,
		2: lapalacian
	}
	input_var = str(" ")
	while(input_var != 'q'):
		print "Function options:"
		
		print options #this is temporary, we'll get a nicer way to print options later.
		
		input_var = raw_input("Enter the character of editing choice or 'q' to quit:")
		if input_var.lower() == 'q':
			print "Quitting..."
			exit(0);
		function = mirrorRightToLeft #default function is fliip	
		try:
			function = options[int(input_var)]
		except IndexError:
			print "ERROR: Invalid function option: " + input_var
			print "Input number not mapped to function"
			continue
		except KeyError:
			print "ERROR: Invalid function option: " + input_var
			print "Input number not mapped to function"
			continue
		except ValueError:
			print "ERROR: Input was not an integer or q: " + input_var
			continue
		
		cores = int(raw_input("Enter the number of cores you wish to use:"))
		
		#tell the user what they've chosen
		print "Running " + function.__name__ + " on " +str(cores)+ " cores..." 
		newImg = img.copy()
		currentPix = img.load() # get the pixels
		newPix = newImg.load() # get the pixels
		threads = []
		# Determine how to divide up the image; divide the height of the image by the number of cores
		# e.g., if step comes out to say 75, then each process will work on 75 pixels (height-wise)
		step = height//cores
		remaining = height%cores
		start = time.time()
		currentLine = 0
		for i in range(cores):
			# Every process will get the same width, but a different height
			lines = step # the minimum number of lines a thread will take
			if(remaining > 0): #if there are remaining lines, add 1 to lines and remove from remaining
				lines = lines + 1
				remaining = remaining - 1
			currentLine = currentLine + lines
			t = threading.Thread(target= function,args = [width, currentLine, lines, que])
			threads.append(t)
			t.start()


		for t in threads:
			t.join()
		
		

		print("Elapsed time:", round(time.time() - start, 5))
		
		# Show new image
		#newImg.show()
		newFName = "NewImage" + str(imageNumber) + ".png"
		newImg.save(newFName);
		imageNumber = imageNumber+1
		print "Image saved as: " + newFName
		img = newImg

if __name__ == "__main__":
	main()
