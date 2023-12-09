import os
import cv2
import numpy as np
from main import x_real, y_real, z_real, images_path

# camera ports corresponding to xy, z
cam_ports = [0, 1]

for i in cam_ports:

    # initialize the camera
    cam = cv2.VideoCapture(i)

    # reading the input
    ret, img = cam.read()

    if ret:

        # if image was detected without any error, transform
        if i == cam_ports[0]:

                # locate points of the usable range and map them
                pts1 = np.float32([[272, 91], [504, 92],
                                   [271, 271], [510, 270]])
                pts2 = np.float32([[x_real, y_real], [0, y_real],
                                   [x_real, 0], [0, 0]])

                # apply Perspective Transform Algorithm
                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                result = cv2.warpPerspective(img, matrix, (x_real, y_real))
                
        elif i == cam_ports[1]:
        
                pts1 = np.float32([[197, 33], [628, 34],
                                   [198, 413], [629, 406]])
                pts2 = np.float32([[0, 0], [y_real, 0],
                                   [0, z_real], [y_real, z_real]])

                matrix = cv2.getPerspectiveTransform(pts1, pts2)
                result = cv2.warpPerspective(img, matrix, (y_real, z_real))

        # saving image in local storage
        cv2.imwrite(os.path.join(images_path, f'exp_port_{i}.jpg'), result)
        cv2.waitKey(0)

    else:
        print("ERROR: No image detected")