#!/usr/bin/env python
# -*- coding: utf-8 -*

#sudo apt-get install python3-flask
#pip3 install opencv-python

import os
from flask import Flask, render_template, Response
import cv2
from time import sleep

app = Flask(__name__)
#app.config["CACHE_TYPE"] = "null"

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/send/<code>')
def send(code):
    os.system('irsend send_once "SamsungMBE131" ' + code)
    print(code, "sent")
    return ('', 204) # 204 is "No Content"


def gen():
    """Video streaming generator function."""
    vs = cv2.VideoCapture(0, cv2.CAP_V4L2)

#Tuning camera settings
#    vs.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
#    vs.set(cv2.CAP_PROP_FPS, 17)
#    vs.set(cv2.CAP_PROP_EXPOSURE, 50)
    vs.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)

    while True:
        ret,frame=vs.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame=jpeg.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#        sleep(0.1)


    vs.release()
    cv2.destroyAllWindows()




@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =5000, debug=True, threaded=True)
