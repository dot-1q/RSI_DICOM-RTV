from pydicom import dcmread
from PIL import Image
import io
import socket
import struct
import time

class Server(object):
    def __init__(self):
        self.frames = []
        self.counter = 0
        ds = dcmread('bio.dcm')
        for i in range(ds.NumberOfFrames):
            frame = ds.pixel_array[i]
            self.frames.append(frame)
        print("Number of frames in self " + str(len(self.frames)))
        
        #Create socket to send the video stream
        self.create_socket()
        self.stream_video()

    def create_socket(self):
       self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

       #Dentro da rede da UA isto provavelmente tem de ser mudado
       port = 9000
       socket_address = ('',port)
       print('Video Socket Created')
       self.server_socket.bind(socket_address)
       print('Video Socket Binded')
       self.server_socket.listen(10)
       print('Video Socket Listening')

    def stream_video(self):
        print("Created video stream")
        client_socket,addr = self.server_socket.accept()
        print('Connection from:', addr)
        
        while True:
            if client_socket:
                image = Image.fromarray(self.frames[self.counter])
                if self.counter < len(self.frames)-1:
                    self.counter +=1
                else:
                    self.counter=0
                buf = io.BytesIO()
                image.save(buf,'JPEG')
                message = struct.pack("Q",len(buf.getbuffer()))+buf.getbuffer()
                client_socket.sendall(message)
                print("Sent Frame {n}".format(n=self.counter))
                time.sleep(0.2)

# Run the server
Server()