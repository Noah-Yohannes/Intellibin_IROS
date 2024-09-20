from tensorflow import keras
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Make sure there is Models/model0 folder
loaded_model = keras.models.load_model('Models/model0')

cam = cv2.VideoCapture(0)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("Webcam", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        # image = cv2.imread(frame)
        image = cv2.resize(frame, (480,270),interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        result = loaded_model.predict(np.array([image/255]))
        predicted_value = "can" if np.argmax(result) else "paper"
        im = cv2.putText(frame,predicted_value,(50,50),cv2.FONT_HERSHEY_COMPLEX,1.5,(0,0,255),3)
        cv2.imshow("Predict", im)
        print(predicted_value)

cam.release()

cv2.destroyAllWindows()