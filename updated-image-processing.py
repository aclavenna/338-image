from PIL import Image
import multiprocessing as mp
import threading
import time

img = Image.open('house.png')
newImg = img.copy()
currentPix = img.load() # get the pixels
newPix = newImg.load() # get the pixels

results = []
def flip(width, height, step, que):
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

	


def main():
	que = mp.Queue()

	width, height = img.size

	cores = mp.cpu_count() # get the number of cores
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
		t = threading.Thread(target= flip,args = [width, currentLine, lines, que])
		threads.append(t)
		t.start()


	for t in threads:
		t.join()
	
	results = []
	

	print("Elapsed time:", round(time.time() - start, 5))
	
	# Show new image
	#newImg.show()
	newImg.save("NewImage.png");

if __name__ == "__main__":
	main()
