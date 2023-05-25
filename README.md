# xArm Object Retrieval Routines

##  General Info

This project utilizes a microphone and Vosk speech recognition to receive a user's voice command, which will activate an overhead camera and run YOLOv5 object detection to locate an object's position. An xArm 5 Lite with a gripper attachment will then execute a retrieval routine and return to its initial position to repeat the process.

<p align="center">
  <img src="https://github.com/ploMG/xArm-2D-Detection/assets/128610413/c0471c78-a205-4b13-ae64-b030bdcbcbda">
</p>
  
There are two routines:

* Manual mode - the user says the name of an object, and the arm will fetch the first instance it can detect. If the object is not detected, the arm will wait idly until an instance is introduced into the environment.

* Automatic mode - the user says "automatic," and the arm will dispose of all instances of trash. If there are no more instances detected, the arm will return to its initial position.

*An important limitation to note is that 2D object detection obtains coordinates for the X and Y plane, so the xArm's Z coordinate position, or the height of the desired object, must be predefined in auto.py and manual.py as the variable rZ. Other parameters can also be adjusted as necessary, such as gripper strength. Check [xArm API](https://github.com/xArm-Developer/xArm-Python-SDK/blob/master/doc/api/xarm_api.md) for more info.*


## Setup

### Vosk

Vosk speech recognition models can be downloaded from the [official page](https://alphacephei.com/vosk/models). This project uses the small US English model.

When main.py is run, an audio stream begins that will continuously transcribe the user's input until a keyword to activate a retrieval routine is detected.

### Camera

The camera's coordinates are not inherently synced to the xArm's, so commands from the OpenCV library are used to correct the images it takes before running YOLOv5. Calibration is done by taking images of the arm at each of the four corners of the defined environment and finding the pixel coordinates.

<p align="center">
  <img src="https://github.com/ploMG/xArm-2D-Detection/assets/128610413/1d47ea77-cd9d-4987-bfbb-1c3494917e13">
</p>

### YOLOv5

After downloading [YOLOv5](https://github.com/ultralytics/yolov5), the default detect.py should be replaced by the modified detect.py found in the scripts folder. The YOLOv5 train.py script can be used to train the model, and images for a custom dataset can be gathered using the traindata.py script. This project uses a dataset that differentiates between bottles and crushed bottles (trash). The testing, training, and validation images and labels are found in the data folder. Generated result figures from running train.py with this data is available in the images folder.

After detecting an object, the generated bounding box coordinates will be used to calculate the arm's X and Y position.

<p align="center">
  <img src="https://github.com/ploMG/xArm-2D-Detection/assets/128610413/3f577b51-995b-4418-9c5c-0a188fcb12a9">
</p>


## Samples

https://github.com/ploMG/xArm-2D-Detection/assets/128610413/51946f42-1930-4df6-95a6-03c7511d5516

> Automatic mode demonstration

https://github.com/ploMG/xArm-2D-Detection/assets/128610413/f5670124-a470-45c7-91a2-337205ba0a15

> Manual mode demonstration
