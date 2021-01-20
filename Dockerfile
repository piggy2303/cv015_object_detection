FROM nvidia/cuda:11.1-base-ubuntu20.04
FROM pytorch/pytorch

RUN apt update && DEBIAN_FRONTEND=noninteractive apt install wget python3-pip python3-dev libgl1-mesa-glx -y

RUN pip3 install --upgrade pip

RUN pip install Flask
RUN pip install Flask-Cors==1.10.3
RUN pip install gevent
# RUN pip install matplotlib
# RUN pip install opencv-python
# RUN pip install scikit-image==0.14.2
# RUN pip install scipy
# RUN pip install googledrivedownloader
# RUN pip install fastai==2.1.7

RUN pip install cmake --upgrade
ADD . /app
WORKDIR /app
RUN ./build.sh
RUN wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights


CMD python3 wsgi.py
