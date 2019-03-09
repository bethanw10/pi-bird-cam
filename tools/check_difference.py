import time
import datetime
import picamera
import picamera.array
import os
import matplotlib.pyplot as plot
from fractions import Fraction

# Motion Settings
threshold = 45   # How Much a pixel has to change

# Camera Settings
testWidth = 128
testHeight = 80

# Tool for calculating what the total number of changed pixels would have been for each stream
def calculateDifference(data1, data2):
    # Find motion between two data streams based on sensitivity and threshold
    motionDetected = False
    pixColor = 1 # red=0 green=1 blue=2
    pixChanges = 0
    pixDiffs = 0
    numberOverThreshold = 0 
    for w in range(0, testWidth):
        for h in range(0, testHeight):
            # get the diff of the pixel. Conversion to int
            # is required to avoid unsigned short overflow.
            pixDiff = abs(int(data1[h][w][pixColor]) - int(data2[h][w][pixColor]))
            if  pixDiff > threshold:
                pixDiffs += pixDiff
                numberOverThreshold += 1
                pixChanges += 1
                
    print('Changed pixels: ' + str(pixChanges))
    print('Average difference: ' + str(pixDiffs / numberOverThreshold))
    print()


files =  sorted(os.listdir('../streams'))

for i in range(int(len(files) / 2)):
    print(files[i * 2] + " " + files[i * 2 + 1])
    
    baseFile = files[i * 2]
    currentFile = files[i * 2 + 1]
    
    baseImage = plot.imread('../streams/' + baseFile)
    currentImage = plot.imread('../streams/' + currentFile)
    
    calculateDifference(baseImage, currentImage)
    