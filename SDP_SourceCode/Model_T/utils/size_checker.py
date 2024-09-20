import cv2
import PIL
import pathlib
from PIL import Image
import os
folder = pathlib.Path("dcrpi-b")
files = folder.glob("*/*")
target_size = (224, 224)

for file in files:
    # img = cv2.imread(str(file))
    # height,width,_= img.shape
    # print(img.shape)
    # print(str(file))
    # if (height, width)==target_size:
    #     print(str(file))
    try:
        img = Image.open(str(file))
        img.verify()
    except(IOError,SyntaxError) as e :
        os.remove(file)