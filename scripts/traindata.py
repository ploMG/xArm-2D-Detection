import cv2
import numpy as np
import os

# capture single image from webcam

# initialize the camera
# If you have multiple camera connected with
# current device, assign a value in cam_port
# variable according to that
cam_port = 0
cam = cv2.VideoCapture(cam_port)

# reading the input using the camera
ret, img = cam.read()
path = 'D:/Users/Tej/Downloads/yolov5-master/data/images'

#If image was detected without any error, show result
if ret:
        # Locate points of the documents
        # or object which you want to transform
        pts1 = np.float32([[253, 97], [514, 92],
                           [251, 283], [520, 283]])
        pts2 = np.float32([[550, 400], [0, 400],
                           [550, 0], [0, 0]])

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (550, 400))

        # saving image in local storage
        cv2.imwrite(os.path.join(path, 'exp.jpg'), result)
        cv2.waitKey(0)

else:
    print("ERROR: No image detected")