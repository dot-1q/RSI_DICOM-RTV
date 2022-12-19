from flask import Flask, render_template, jsonify, request, Response
from camera import Camera
import time

app = Flask(__name__, static_url_path="/static")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + (frame) + b'\r\n')
        time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(threaded=True)
