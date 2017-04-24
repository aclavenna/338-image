from PIL import Image
import multiprocessing as mp
import threading
import time

img = Image.open('house.png')
newImg = img.copy()
currentPix = img.load() # get the pixels
newPix = newImg.load() # get the pixels

results = []
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


def main():
	que = mp.Queue()

	width, height = img.size

	cores = mp.cpu_count() # get the number of cores
	imageNumber = 0
	#define function options
	options ={
		0: mirrorRightToLeft,
		1: mirrorLeftToRight
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
			
		#tell the user what they've chosen
		print "Running " + function.__name__ + "..."
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
		
		results = []
		

		print("Elapsed time:", round(time.time() - start, 5))
		
		# Show new image
		#newImg.show()
		newFName = "NewImage" + str(imageNumber) + ".png"
		newImg.save(newFName);
		imageNumber = imageNumber+1
		print "Image saved as: " + newFName

if __name__ == "__main__":
	main()
