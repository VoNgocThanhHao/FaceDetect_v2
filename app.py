import cv2
from flask import Flask, render_template, request, redirect, flash
import numpy as np
import serverless_wsgi
import base64

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Trang chủ")

@app.route("/up-load", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    path_input = "/tmp/input.png"
    path_output = "/tmp/output.png"
    file.save(path_input)

    #-----------------------------

    net = cv2.dnn.readNetFromCaffe("./deploy.prototxt", "./res10_300x300_ssd_iter_140000.caffemodel")
    frame = cv2.imread(path_input)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence < 0.5:
            continue
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY),
            (0, 0, 255), 2)
        cv2.putText(frame, text, (startX, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    cv2.imwrite(path_output, frame)

    #-----------------------------

    with open("/tmp/output.png", "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())
    image = b64_string.decode('utf-8')

    return render_template("index.html", image = image, title="Trang chủ")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
