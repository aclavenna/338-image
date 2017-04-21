from PIL import Image
import multiprocessing as mp
import time

img = Image.open('house.png')
img.show() # show original image
pix = img.load() # get the pixels

results = []
def flip(width, height, step, que):
	# Record time for function
	ftime = time.time()
	
	# Array that contains tuples of the form: (XY value, RGB value)
	temp = []

	# make image symmetric about a vertical axis
	for x in range(int(width/2)):
		for y in range(height-step,height):
			pix[x,y] = pix[width-1-x, y]
			temp.append(((x,y), pix[x,y]))
			# img.putpixel((x,y), (pix[x,y]))
	
	# Print time for function to execute
	# print(mp.current_process().name, "time:", round(time.time() - ftime, 5))

	# Put the results in the queue
	que.put(temp)
	
	#img.show()
	

def main():
	que = mp.Queue()

	width, height = img.size
	
	# pixels = []
	# for y in range(height):
	# 	for x in range(width):
	# 		pixels.append([x,y])
	# print(pixels)

	# start = time.time()
	# flip(width, height, 1, que)
	# print("Elapsed time:", round(time.time() - start, 5))


	cores = mp.cpu_count() # get the number of cores
	processes = []

	# Determine how to divide up the image; divide the height of the image by the number of cores
	# e.g., if step comes out to say 75, then each process will work on 75 pixels (height-wise)
	step = int(height/cores)

	start = time.time()
	for i in range(0, height, step):
		# Every process will get the same width, but a different height
		p = mp.Process(name = "process" + str(i), target = flip, args = [width, i+step, step, que])
		processes.append(p)
		p.start()

	''' For some reason, uncommenting this will cause the program to hang. 
		It has to do with the size of the arrays that we are adding into the queue.'''	
	# for p in processes:
	# 	p.join()
	
	results = []
	
	for i in range(len(processes)):
		# get an array of pixels from the queue
		temp = que.get()

		# Assign the new pixels to the image
		# Because 'temp' is such a large array, this for loop takes a significant amount of time
		for j in range(len(temp)):
			# temp[j][0] is the XY value; temp[j][1] is the RGB value
			img.putpixel(temp[j][0], temp[j][1])

	print("Elapsed time:", round(time.time() - start, 5))
	
	# Show new image
	img.show()
	

if __name__ == "__main__":
	main()
