import cv2
import numpy as np
import os
import sys
sys.path.insert(1, r".../yolov5-master/") #insert path to YOLOv5 here, ctrl+F "..." or replace all

# capture single image from webcam

# initialize the camera
# If you have multiple camera connected with
# current device, assign a value in cam_port
# variable according to that
cam_port = 0
cam = cv2.VideoCapture(cam_port)

# Read the user's request
with open("transcription.txt", 'r') as t:
    tr = t.read()
    t.close()

# Clear results from previous runs
clear_return = open(r"...\yolov5-master\return.txt", 'w')
clear_return.close()
clear_points = open(r"...\yolov5-master\points.txt", 'w')
clear_points.close()

object_name = ""

# Loop will continue until the requested object is detected
while tr != object_name:

    # Reading the input using the webcam
    ret, img = cam.read()
    path = '.../yolov5-master/data/images'

    # If image was captured, then transform and detect
    if ret:

        # Corner points of original capture
        pts1 = np.float32([[253, 97], [514, 92],
                           [251, 283], [520, 283]])

        # Mapped to transformed corner points
        pts2 = np.float32([[550, 400], [0, 400],
                           [550, 0], [0, 0]])

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (550, 400))  # Domain and range of workspace

        # Saving image in local storage
        cv2.imwrite(os.path.join(path, 'exp.jpg'), result)
        cv2.waitKey(0)

        # YOLOv5 detection on exported image
        os.system('cmd /c "cd ...\\yolov5-master & python detect.py --source ...\\yolov5-master\\data\\images\\exp.jpg --weights ...\\yolov5-master\\runs\\train\\bottle_det\\weights\\best.pt --conf 0.25"')

        # Read bounding box coordinates
        with open(r"...\yolov5-master\points.txt", 'r') as point:
            coor = point.read().split()
            point.close()

        # Read bounding box label
        with open(r"...\yolov5-master\return.txt", 'r') as label:
            object_name = label.read()
            label.close()

    # If captured image is corrupted, throw error
    else:
        print("ERROR: No image detected")

coor = [int(i) for i in coor]

# Translate bbox coordinates to xArm coordinates
rX = (coor[0] + coor[2]) / 2
rY = ((400 - coor[1]) + (400 - coor[3])) / 2

if tr == "bottle":
    rZ = 300
    rG = 250
#elif tr == :
#    rZ =
#    rG =

#go to object
print(arm.set_position(x=rX, y=rY, z=399.3, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
#print(arm.set_servo_angle(servo_id=5, angle=120, is_radian=False, wait=True))
code = arm.set_gripper_position(850, wait=True, speed=2000)
print('[wait]set gripper pos, code={}'.format(code))
print(arm.set_position(x=rX, y=rY, z=rZ, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
arm.clean_error()
time.sleep(0.5)
arm.set_state(0)

# grip and go to drop point
code = arm.set_gripper_position(rG, wait=True, speed=2000)
print('[no wait]set gripper pos, code={}'.format(code))
print(arm.set_position(x=255.2, y=0, z=486.5, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
print(arm.set_position(x=255.2, y=0, z=rZ, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
arm.clean_error()
time.sleep(0.5)
arm.set_state(0)
