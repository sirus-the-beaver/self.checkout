from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils

# edge detection
image = cv2.imread("../scan.jpg") # read image
ratio = image.shape[0] / 500.0 # calculate ratio of old height to new height
orig = image.copy() # make a copy of the original image
image = imutils.resize(image, height=500) # resize image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert image to grayscale
gray = cv2.bilateralFilter(gray, 11, 17, 17) # apply bilateral filter to remove noise
gray = cv2.medianBlur(gray, 5) # apply median blur to smooth the edges
edged = cv2.Canny(gray, 30, 400) # apply canny edge detection algorithm

# find contours in the edged image, keep only the largest ones, and initialize our screen contour
contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # find contours

# approximate the contour
contours = sorted(contours, key=cv2.contourArea, reverse=True) # sort contours by area

screenCntList = []
scrWiths = []

for c in contours:
    peri = cv2.arcLength(c, True) # calculate perimeter of contour
    approx = cv2.approxPolyDP(c, 0.02 * peri, True) # approximate the contour

    # if our approximated contour has four points, then we can assume that we have found our screen
    if len(approx) == 4:
        (X, Y, W, H) = cv2.boundingRect(c)
        screenCntList.append(approx)
        scrWiths.append(W)

        break

# get the largest screen contour
screenCntList, scrWiths = findLargestContour(screenCntList, scrWiths)

# apply the four point transform to obtain a top-down view of the original image
points = screenCntList[0].reshape(4, 2)

# define the rectangle of the new image
rect = order_points(points)

warped = four_point_transform(orig, screenCntList[0].reshape(4, 2) * ratio)