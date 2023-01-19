from flask import Flask, render_template,Response
import socket
import struct
import pyaudio
import pydicom

app = Flask(__name__, static_url_path="/static")
client_socket1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.0.1'
port = 9000

client_socket1.connect((host_ip,port))
payload_size = struct.calcsize("Q")

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
audio1 = pyaudio.PyAudio()

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(video_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio')
def audio():
    # start Recording
    def sound():

        CHUNK = 1024
        sampleRate = 44100
        bitsPerSample = 16
        channels = 2
        wav_header = genHeader(sampleRate, bitsPerSample, channels)

        stream = audio1.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,input_device_index=14,
                        frames_per_buffer=CHUNK)
        print("recording...")
        first_run = True
        while True:
           if first_run:
               data = wav_header + stream.read(CHUNK,exception_on_overflow=False)
               first_run = False
           else:
               data = stream.read(CHUNK)
           yield(data)

    return Response(sound())

def video_frames():
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

def genHeader(sampleRate, bitsPerSample, channels):
    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5000',threaded=True)
