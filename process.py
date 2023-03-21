import numpy as np
import cv2

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def edge(input_image):
    image = input_image
    image = ResizeWithAspectRatio(image, height=720)
    image = cv2.medianBlur(image, 3, 0)

    #for row,i in enumerate(image):
        #for col,j in enumerate(i):
            #for channel,k in enumerate(j):
                #image[row][col][channel] = (image[row][col][channel]//32)*32
        #print("Progress: " + str(row/len(image)))
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = cv2.Canny(image,100,200,1)
    image = cv2.dilate(image, None, iterations=2)
    image = cv2.erode(image, None, iterations=2)
    return image