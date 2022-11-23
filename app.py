"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
from query import update, select
import threading
from flask import Flask, render_template, Response
import torch
import io
from PIL import Image
import cv2
import numpy as np
from time import sleep

app = Flask(__name__)

# Load Pre-trained Model
model = torch.hub.load(
    "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
)  # .autoshape()  # force_reload = recache latest code

# Load Custom Model
# model = torch.hub.load("ultralytics/yolov5", "custom",
#                        path="./best.pt", force_reload=True)

# Set Model Settings
model.eval()
model.conf = 0.6  # confidence threshold (0-1)
model.iou = 0.45  # NMS IoU threshold (0-1)

# 강아지 iptime ipcam
# cap = cv2.VideoCapture(
#     "rtsp://dogcam:blueberry19@errong.iptimecam.com:21040/stream_ch00_0")

# 브라이튼 iptime ipcam
# cap = cv2.VideoCapture(
#     "rtsp://brighten:brighten0701@192.168.0.44:554/stream_ch00_0")

# webcam
cap = cv2.VideoCapture(1)

# pi camera
# 오류 발생 시 sudo service nvargus-daemon restart


def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


# cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)

''' 멀티 스레드로 object detection(yolo) 돌리고 http 요청 들어오면 화면 송출 '''

results = None
lst = []


def detect():
    global results
    global lst
    global cap
    while (cap.isOpened()):
        # Capture frame-by-fram ## read the camera frame
        success, frame = cap.read()
        if success == True:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            img = Image.open(io.BytesIO(frame))

            ''' 학습한 이미지 사이즈 맞추기 '''
            results = model(img, size=640)

            # results.print()  # print results to screen

            lst = []
            df = results.pandas().xyxy[0]
            for i in df['name']:
                update(i)
                lst.append(i)
            print(lst)
        else:  # reload when no frame
            cap = cap
            sleep(3)


def gen():
    global results
    while (cap.isOpened()):
        # convert remove single-dimensional entries from the shape of an array
        img = np.squeeze(results.render())  # RGB
        # read image as BGR
        img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # BGR

        # Encode BGR image to bytes so that cv2 will convert to RGB
        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()
        # print(frame)
        sleep(0.03)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/database')
def show():
    return select()


if __name__ == "__main__":
    detect_thread = threading.Thread(target=detect)
    detect_thread.start()

    app.run(host='0.0.0.0', port=5000)
