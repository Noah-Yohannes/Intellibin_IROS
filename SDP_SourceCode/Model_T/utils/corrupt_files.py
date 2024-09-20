#remove corrupt images    
import pathlib
import PIL
from PIL import Image
import os
dir_path = pathlib.Path("Training Set")
files = dir_path.glob("*/*")
count = 0
for file in files:
  try:
    img = Image.open(file)
    img.verify()
  except (IOError,SyntaxError) as e:
    print(str(file))
    os.remove(file)
    count = count + 1
print(count)