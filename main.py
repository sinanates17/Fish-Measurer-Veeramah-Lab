import os
from measure import processImage
from cv2 import waitKey

#This is the pseudocode for fish measurement

#Obtain a list of fish images 
inDirectory = os.getcwd() + "/Input"

Inputs = os.listdir(inDirectory)


#Loop through every image path in the list
for image in Inputs:

    #Create an output file labelled with the name of the image.

        processImage(inDirectory + "/" + image, 1.905)
waitKey(0)
        

