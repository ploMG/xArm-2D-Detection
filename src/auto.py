import os
import sys
import cv2
import numpy as np
from main import x_real, y_real, z_real, xmin, ymin, ymax, zmin, zmax, cz, cam_x, dX, dY, dZ,\
    yolo_main_path, images_path, return_path, points_path, trained_weights_path
sys.path.insert(1, yolo_main_path)

# Camera ports corresponding to overhead, lateral
cam_ports = [0, 1]

# Clear results from previous runs
def clear():
    clear_return = open(return_path, 'w')
    clear_return.close()
    clear_points = open(points_path, 'w')
    clear_points.close()

def remove():
    # go to object
    print(arm.set_position(x=rX, y=rY, z=zmax, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    # print(arm.set_servo_angle(servo_id=5, angle=120, is_radian=False, wait=True))
    code = arm.set_gripper_position(850, wait=True, speed=2000)
    print('[wait]set gripper pos, code={}'.format(code))
    print(arm.set_position(x=rX, y=rY, z=rZ, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    arm.clean_error()
    time.sleep(0.5)
    arm.set_state(0)

    # grip and go to drop point
    code = arm.set_gripper_position(rG, wait=True, speed=2000)
    print('[no wait]set gripper pos, code={}'.format(code))
    print(arm.set_position(x=rX, y=rY, z=zmax, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    print(arm.set_position(x=dX, y=dY, z=dZ, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    arm.clean_error()
    time.sleep(0.5)
    arm.set_state(0)

    # Release and return
    print(arm.set_gripper_position(850, wait=True, speed=2000))
    print(arm.set_position(x=250, y=0, z=zmax, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    arm.clean_error()
    time.sleep(0.5)
    arm.set_state(0)

object_name = "trash"

# Loop will continue until all trash is removed
while object_name == "trash":

    clear()

    # Reading the input using the webcam
    cam = cv2.VideoCapture(cam_ports[0])
    ret, img = cam.read()

    # If image was captured, then transform and detect
    if ret:

        # Corner points of original capture
        pts1 = np.float32([[272, 91], [504, 92],
                           [271, 271], [510, 270]])

        # Mapped to transformed corner points
        pts2 = np.float32([[x_real, y_real], [0, y_real],
                           [x_real, 0], [0, 0]])

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (x_real, y_real))  # Domain and range of workspace

        # Saving image in local storage
        export_path = (os.path.join(images_path, f'exp_port_{cam_ports[0]}.jpg'))
        cv2.imwrite(export_path, result)
        cv2.waitKey(0)

        # YOLOv5 detection on exported image
        os.system(f'cmd /c "{yolo_main_path[:2]} & cd {yolo_main_path.replace("/", chr(92))} & python detect.py --source {export_path.replace("/", chr(92))} --weights {trained_weights_path.replace("/", chr(92))} --conf 0.25"')

        # Read bounding box coordinates
        with open(points_path, 'r') as point:
            coor = point.read().split()
            point.close()

        # Read bounding box label
        with open(return_path, 'r') as label:
            object_name = label.read()
            label.close()

    # If captured image is corrupted, throw error
    else:
        print("ERROR: No image detected")

    if object_name == "trash":
        coor = [int(i) for i in coor]

        # Translate bbox coordinates to xArm coordinates
        rX = (coor[0] + coor[2]) / 2 + xmin
        rY = ((ymax - coor[1]) + (ymax - coor[3])) / 2 + ymin

        clear()

        # Reading input for secondary camera
        cam = cv2.VideoCapture(cam_ports[1])
        ret, img = cam.read()

        if ret:

            pts1 = np.float32([[197, 33], [628, 34],
                                [198, 413], [629, 406]])
            pts2 = np.float32([[0, 0], [y_real, 0],
                                [0, z_real], [y_real, z_real]])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            result = cv2.warpPerspective(img, matrix, (y_real, z_real))  # Domain and range of workspace

            export_path = (os.path.join(images_path, f'exp_port_{cam_ports[1]}.jpg'))
            cv2.imwrite(export_path, result)
            cv2.waitKey(0)

            # YOLOv5 detection on exported image
            os.system(f'cmd /c "{yolo_main_path[:2]} & cd {yolo_main_path.replace("/", chr(92))} & python detect.py --source {export_path.replace("/", chr(92))} --weights {trained_weights_path.replace("/", chr(92))} --conf 0.25"')

            # Read bounding box coordinates
            with open(points_path, 'r') as point:
                coor = point.read().split()
                point.close()

            # Read bounding box label
            with open(return_path, 'r') as label:
                object_name = label.read()
                label.close()

        # If captured image is corrupted, throw error
        else:
            print("ERROR: No image detected")

        if object_name == "trash":
            coor = [int(i) for i in coor]

            scale = 2 ** (-rX / cam_x)
            rZ = (coor[3] - coor[1]) / scale + zmin - cz
            rG = (coor[2] - coor[0]) / scale

            print('rX:', rX)
            print('rY:', rY)
            print('rZ:', rZ)
            print('rG:', rG)

            remove()

        else:
            print("\nNo trash detected\n")

    else:
        print("\nNo trash detected\n")