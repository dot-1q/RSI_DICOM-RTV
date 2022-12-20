from flask import Flask, render_template, jsonify, request, Response
from threading import Thread
import socket
import struct

app = Flask(__name__, static_url_path="/static")
client_socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.0.1'
port = 9002

client_socket1.connect((host_ip,port))
client_socket2.connect((host_ip,port+1))
payload_size = struct.calcsize("Q")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

def gen():
    data = b''
    while True:
        while len(data) < payload_size:
            packet = client_socket1.recv(4*1024)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket1.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = frame_data
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + (frame) + b'\r\n')

def gen2():
    data = b''
    while True:
        while len(data) < payload_size:
            packet = client_socket2.recv(4*1024)
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket2.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = frame_data
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + (frame) + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed2')
def video_feed2():
    return Response(gen2(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(threaded=True)
