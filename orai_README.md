# Real-time object detection

Input: an image
Ouput: rois and labels of detected objects

## Requirements

- Linux
- CMake
- g++

## Setup

- Download and compile darknet (YOLOv4)
```
git clone https://github.com/AlexeyAB/darknet.git
cd darknet
make
```
You will see a `darknet` exe file inside `darknet` dir

- Download weight (YOLOv4 tiny)
```
wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
```

## Run

- Run a test image e.g. `test/traffic.jpg`
```
./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights test/traffic.jpg -dont_show -ext_output
```
We will get objects and their bounding boxes and a result image

## Modify code to change name of output file to avoid conflict

Default output name is `predictions.jpg` in the same folder.
```
Line 372 in src/coco.c
save_image(im, "prediction");
show_image(im, "predictions");
```

## Refs

https://robocademy.com/2020/05/01/a-gentle-introduction-to-yolo-v4-for-object-detection-in-ubuntu-20-04/
