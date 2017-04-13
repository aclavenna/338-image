from PIL import Image, ImageFilter 
import multiprocessing as mp
import time



img = Image.open('house.png')
img.show() # show original image
pix = img.load() # get the pixels

#print(pix[100,346]) # Passing an x and y value to pix will return a tuple of the form (R, G, B)

# This function makes the image (or part of the image) vertically symmetric
def flip(width, height):
	for x in range(int(width/2)):
		for y in range(height):
			pix[x,y] = pix[width-1-x, y]
	img.save('new-house.png')
	'''uncommenting the following the statement will show the result of each process'''
	#img.show()              

def main():
        input_var = ""
        while input_var != "3": #keeps continuing loop until user want to quit proggram
                input_var = input("Enter the number of editing choice:\n 1: flip\n 2: blur\n 3: quit\n")
                if input_var == "3": #quit program
                        print("Quit processed.")
                                
                elif input_var != "3":
                        
                        while not ("0" < input_var < "4"): #ensures valid entry
                                print("Invalid entry.\n")
                                input_var = input("Enter the number of editing choice:\n 1: flip\n 2: blur\n 3: quit\n")  

                        if input_var == "1":
                                function = flip
                                
                        elif input_var == "2":
                                function = blur

                                
                        width, height = img.size
                        cores = mp.cpu_count() # get the number of cores
                        processes = []

                        for i in range(0, height, int(height/cores)):#range(0, height, steps-->int(height/cores))
                                p = mp.Process(name = str(input_var) + str(i), target = function, args = [width, i+int(height/cores)]) 
                                processes.append(p)
                                p.start()

                        for p in processes:
                                p.join()
                        Image.open('new-house.png').show()

                        

if __name__ == "__main__":
	main()
