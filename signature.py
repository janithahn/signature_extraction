import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import getopt, sys

# taking file inputes with command line arguments
argumentList = sys.argv[1:]
short_options = "hi:o:"
long_options = ["Input=", "Output="]
inputFile = ''
outputFile = ''

try:
    opts, args = getopt.getopt(argumentList, short_options, long_options)
    for opt, arg in opts:
        if opt in ('-h', '--Help'):
            print('signature.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--Input'):
            inputFile = arg
        elif opt in ('-o', '--Output'):
            outputFile = arg
except getopt.error as err:
    print (str(err))
    sys.exit(2)

# taking the image input
originalImg = cv.imread('input/' + inputFile)
originalGray = cv.cvtColor(originalImg, cv.COLOR_BGR2GRAY)
img = cv.threshold(originalGray, 127, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

scale_percent = 50

width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)

resized = cv.resize(img, (width, height))

# cv.imshow('resized thresh image', resized)

# looking for connected components
# https://scipy-lectures.org/packages/scikit-image/auto_examples/plot_labels.html
blobs = img > img.mean()
blobs_labels = measure.label(blobs, background=1)
image_label_overlay = label2rgb(blobs_labels, image=img)

plt.imshow(image_label_overlay)
plt.title('image_label_overlay')
plt.axis('off')
# plt.show()

# https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_regionprops.html
regions = regionprops(blobs_labels)
totalArea = 0
count = 0

for region in regions:
    if (region.area > 10):
        totalArea += region.area
        count += 1

minSize = (((totalArea/count)/75) * 280) + 85

smallObjectsRemoved = morphology.remove_small_objects(blobs_labels, min_size=minSize, connectivity=1, in_place=False)

plt.imsave('temp/before_final.png', smallObjectsRemoved)

before_final = cv.imread('temp/before_final.png', 0)

finalImg = cv.threshold(before_final, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]

cv.imwrite('output/final.png', finalImg)

############################ SIGNATURE CROP ############################

img = cv.imread('output/final.png')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

retval, thresh_gray = cv.threshold(gray, thresh=100, maxval=255, type=cv.THRESH_BINARY_INV)

canny = cv.Canny(thresh_gray, 150, 120)
kernel = np.ones((55, 55), np.uint8)
closing = cv.morphologyEx(canny, cv.MORPH_CLOSE, kernel)

contours, hierarchy = cv.findContours(closing, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

print('contours:', len(contours))

for (i,c) in enumerate(contours):
    cArea = cv.contourArea(c)
    x, y, w, h = cv.boundingRect(c)

    if((w * h) > (minSize * 5)):
        croppedContour = img[y:y+h, x:x+w]
        imageName = 'img_cropped' + str(i+1) + '.jpg'
        cv.rectangle(originalImg, (x,y), (x+w,y+h), (200,0,0), 2)
        cv.imwrite('output/'+ imageName, croppedContour)

# Find object with the biggest bounding box
'''mx = (0,0,0,0)
mx_area = 0
for cont in contours:
    x,y,w,h = cv.boundingRect(cont)
    area = w*h
    if area > mx_area:
        mx = x,y,w,h
        mx_area = area
x,y,w,h = mx

# Output to files
roi = img[y:y+h, x:x+w]
cv.imwrite('Image_crop.jpg', roi)'''

b, g, r = cv.split(originalImg)
originalImg = cv.merge([r, g, b])

plt.imshow(originalImg)
plt.title('img')
plt.axis('off')
plt.show()

# cv.imwrite("final.png", finalImg)

cv.waitKey()
