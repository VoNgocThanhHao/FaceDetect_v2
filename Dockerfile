FROM python:3.6.9
WORKDIR /FaceDetect_v2
ADD . /FaceDetect_v2
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3","app.py"]