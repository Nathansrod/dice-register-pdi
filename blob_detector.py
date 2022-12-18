#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022

import cv2

# Setup SimpleBlobDetector parameters
params = cv2.SimpleBlobDetector_Params()

# Simple blobDetector works by: Thresholding -> Grouping -> Merging -> Calculating Center + raius
# of pixels that share common propeties in the image.

# Configuring parameters

# Min and max thresholds to be used when thresholding the image
params.minThreshold = 10;
params.maxThreshold = 255;

# Enables area filter. Searches for blobs with area >= minArea
params.filterByArea = True
params.minArea = 30

# Enables circularity filter. Measures how close to a circle the blob is. Circle = 1, Square = 0.785 c = (4pi x Area) / (perimeter)²
params.filterByCircularity = True
params.minCircularity = 0.80

# Enables convexity filter. Area of the blob / Area of it's hull (filled circles or partial circles)
params.filterByConvexity = True
params.minConvexity = 0.7

# Enables inertial filter. How elongated the shape is (circle = 1, ellipsis between 0 and 1)
params.filterByInertia = True
params.minInertiaRatio = 0.5

# Creating the detector

def create_detector():
    ver = (cv2.__version__).split('.')
    if int(ver[0] == '3'):
        detector = cv2.SimpleBlobDetector(params)
    else:
        detector = cv2.SimpleBlobDetector_create(params)
    
    return detector

#Autor: Nathan Silva Rodrigues
#Disciplina: PDI - EngComp 2022/02
#Data: Dezembro 2022