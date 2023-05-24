from xarm.wrapper import XArmAPI
from configparser import ConfigParser
from vosk import Model, KaldiRecognizer

import os
import sys
import time
import pyaudio

sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

#######################################################
if len(sys.argv) >= 2:
    ip = sys.argv[1]
else:
    try:
        parser = ConfigParser()
        parser.read('D:/Users/Tej/Downloads/xArm-Python-SDK-master/example/wrapper/robot.conf')
        ip = parser.get('xArm', 'ip')
    except:
        ip = input('Please input the xArm ip address:')
        if not ip:
            print('input error, exit')
            sys.exit(1)
########################################################

arm = XArmAPI(ip)
time.sleep(0.5)
if arm.warn_code != 0:
    arm.clean_warn()
if arm.error_code != 0:
    arm.clean_error()

arm.connect()
arm.motion_enable(True)
arm.clean_error()
arm.set_mode(0)
arm.set_state(0)
time.sleep(1)

# Reduced mode
code = arm.set_reduced_max_joint_speed(180)
print('set_reduced_max_joint_speed, code={}'.format(code))
arm.set_reduced_max_tcp_speed(500)
print('set_reduced_max_tcp_speed, code={}'.format(code))
arm.set_reduced_mode(True)
print('set_reduced_mode, code={}'.format(code))

# Arm parameters
code = arm.set_tcp_load(weight=0.82, center_of_gravity=[0, 0, 48])
print('set_tcp_load, code={}'.format(code))
arm.set_self_collision_detection(on_off=True)
print('set_self_collision_detection, code={}'.format(code))

# Gripper parameters
code = arm.set_gripper_mode(0)
print('set gripper mode: location mode, code={}'.format(code))
arm.set_gripper_enable(True)
print('set gripper enable, code={}'.format(code))
arm.set_gripper_speed(100)
print('set gripper speed, code={}'.format(code))


# Go to start position
def start():
    arm.clean_error()
    time.sleep(0.5)
    arm.set_state(0)
    print(arm.set_gripper_position(10, wait=True, speed=2000))
    print(arm.set_position(x=255.2, y=0, z=486.5, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    # print(arm.set_servo_angle(servo_id=5, angle=90, is_radian=False, wait=True))
    arm.clean_error()
    time.sleep(0.5)
    arm.set_state(0)


# Release and return
def end():
    print(arm.set_gripper_position(850, wait=True, speed=2000))
    print(arm.set_position(x=255.2, y=0, z=486.5, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    print(arm.set_gripper_position(10, wait=True, speed=2000))
    print(arm.set_position(x=0, y=0, z=500, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))
    arm.clean_error()
    time.sleep(0.5)
    arm.set_state(0)


model = Model(r"D:/Users/Tej/Programs/Anaconda3/envs/env_full/Lib/site-packages/vosk/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# Objects that the user can select
OBJECTS = ["bottle"]

print("\nPlease say which object to retrieve, or say 'automatic' to begin autoremoval mode.\n")

while True:
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):

        text = recognizer.Result()

        # if a keyword is recognized, search and retrieve the object
        if any(word in text for word in OBJECTS):
            object = [word for word in OBJECTS if word in text]
            selection = object[0]
            print(f"\nRetrieving {selection}\n")

            start()

            # Write user selection to readable txt
            with open('transcription.txt', 'w') as f:
                f.write(f"{selection}")
                f.close()

            # Run retrieval routine
            with open("manual.py") as a:
                exec(a.read())

            end()

        elif "automatic" in text:

            print(f"\nBeginning autoremoval\n")

            start()

            # Write user selection to readable txt
            with open('transcription.txt', 'w') as f:
                f.write(f"trash")
                f.close()

            # Run removal routine
            with open("auto.py") as a:
                exec(a.read())

            print(arm.set_gripper_position(10, wait=True, speed=2000))
            print(arm.set_position(x=0, y=0, z=500, roll=180, pitch=0, yaw=0, is_radian=False, wait=True))