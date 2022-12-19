import matplotlib.pyplot as plt
from pydicom import dcmread

ds = dcmread('bio.dcm')
for i in range(ds.NumberOfFrames):
    frame = ds.pixel_array[i]
    print(type(frame))
    plt.imshow(frame)
    plt.show()