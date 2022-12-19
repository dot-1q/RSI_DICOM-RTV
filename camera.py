from time import time
import matplotlib.pyplot as plt
from pydicom import dcmread
from PIL import Image
from io import BytesIO

class Camera(object):
    def __init__(self):
        self.frames = []
        self.counter = 0
        ds = dcmread('bio.dcm')
        for i in range(ds.NumberOfFrames):
            frame = ds.pixel_array[i]
            self.frames.append(frame)
        print("Number of frames in self " + str(len(self.frames)))

    def get_frame(self):
        print("Frame {n}".format(n=self.counter))
        image = Image.fromarray(self.frames[self.counter])
        if self.counter < len(self.frames)-1:
            self.counter +=1
        else:
            self.counter=0
        buf = BytesIO()
        image.save(buf,'JPEG')
        return buf.getbuffer()