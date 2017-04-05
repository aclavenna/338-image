from PIL import Image
import multiprocessing as mp
import time

img = Image.open('house.png')
img.show() # show original image
pix = img.load() # get the pixels

#print(pix[100,346]) # Passing an x and y value to pix will return a tuple of the form (R, G, B)

# This function makes the image (or part of the image) vertically symmetric
def flip(width, height):
	for x in range(width):
		for y in range(height):
			pix[x,y] = pix[width-1-x, y]
	img.save('new-house.png')
	
	'''uncommenting the following the statement will show the result of each process'''
	#img.show()

def main():
	width, height = img.size
	
	# pixels = []
	# for y in range(height):
	# 	for x in range(width):
	# 		pixels.append([x,y])

	cores = mp.cpu_count() # get the number of cores
	processes = []
	for i in range(0, height, int(height/cores)):
		p = mp.Process(name = "flip" + str(i), target = flip, args = [width, i+int(height/cores)])
		processes.append(p)
		p.start()
	for p in processes:
		p.join()
	Image.open('new-house.png').show() #show the new image
	

if __name__ == "__main__":
	main()
	#img.show() # show the new image
