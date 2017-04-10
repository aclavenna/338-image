from PIL import Image, ImageFilter ###
import multiprocessing as mp
import time



###img = Image.open('house.png')
###img = img.filter(ImageFilter.BLUR)


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
        ###how do we only save 1 pic, not 1 pic for each process
        ###use a loop to give user options for image editing
        ###enter file name 
        input_var = input("Enter filename: ")###
        input_var2 = input("Enter edit option: ")###
        print(input_var)###
        
        if (input_var == "flip"):
            width, height = img.size
	# pixels = []
	# for y in range(height):
	# 	for x in range(width):
	# 		pixels.append([x,y])
            cores = mp.cpu_count() # get the number of cores
            processes = []
        ###change the process name of the string according to the function entered
        ###eliminates redundency 
            for i in range(0, height, int(height/cores)):
                    #p = mp.Process(name = "flip" + str(i), target = flip, args = [width, i+int(height/cores)])
                    p = mp.Process(name = str(input_var2) + str(i), target = flip, args = [width, i+int(height/cores)])###
                    processes.append(p)
                    p.start()

            for p in processes:
                    p.join()
            Image.open('new-house.png').show() #show the new image
            ###Image.open(str(input_var)).show() #show the new image
        
	



if __name__ == "__main__":
	main()
