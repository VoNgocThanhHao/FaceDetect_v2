FROM python:3.6.9
RUN apt-get update && apt-get install -y python3-pip
RUN git clone https://github.com/VoNgocThanhHao/FaceDetect_v2.git
RUN cd FaceDetect_v2
WORKDIR /FaceDetect_v2
ADD . /FaceDetect_v2
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]