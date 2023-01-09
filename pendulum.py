import cv2
import numpy as np
import random as rng

#Video to be analysed
vid = cv2.VideoCapture('E:/UTFPR/Fisica Teorica/pendulo.mp4')

#The following function draws contours and finds the central position of a certain "object".
"""Objects are detected by their contours, which are continuous points, around the boundary,
that have similar colours/intensity."""

def getContour(img, file):
    contour, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contour:
        cv2.drawContours(imgCnt, cnt, -1, (255,0,0), 3)

    mu = [None] * len(contour)
    mc = [None] * len(contour)
    for i in range(len(contour)):
        mu[i] = cv2.moments(contour[i])
    for i in range(len(contour)):
        #Adding 1e-5 avoids divisor value equal to zero.
        mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))
        position = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5))
        if position != 0.0:
            print(position)
            file.write('%f \n' % position)


    drawing = np.zeros((img.shape[0], imgCnt.shape[1], 3), dtype=np.uint8)

    for i in range(len(contour)):
        colour = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv2.drawContours(drawing, contour, i, colour, 2)
        cv2.circle(drawing, (int(mc[i][0]), int(mc[i][1])), 4, colour, -1)


#The main loop contains the algorithm that analyses each video's frame
file = open('positions.txt', 'w+')
while True:
    success, img = vid.read()
    img = cv2.resize(img, (550, 550))
    cv2.imshow("Original video", img) #Original video

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Putting the frame in a gray scale makes it easier to determinate lighter and darker pixels

    imgBlur = cv2.GaussianBlur(imgGray, (9, 9), 2)
    #Blurring makes the object's boundary softer and less cracky

    imgCanny = cv2.Canny(imgBlur, 50, 50)
    #Finds the boundaries of the object

    imgCnt = img.copy()
    getContour(imgCanny, file)
    cv2.imshow("Final video", imgCnt)

    if cv2.waitKey(1) & 0xFF == ord('q'): #Condition to run the loop
        break