import time
import ultrasonic
import cam_predict
import tensorflow as tf
# import picamera
# import picamera.array
from servo import *

import cv2

DIST_THRES = 10.0 # cm
class_names = ['Can','Paper','Plastic','General Waste']

cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(2)
assert cam0.isOpened(),"cam0 is not opened"
assert cam1.isOpened(),"cam1 is not opened"

cam0.set(3,224)
cam0.set(4,224)
cam1.set(3,224)
cam1.set(4,224)



cv2.namedWindow("0")
cv2.namedWindow("1")

def main():
    classify_lite = cam_predict.init_pred()

    i = 0
    start = time.time()

    while True:
        _,frame0 = cam0.read()
        _,frame1 = cam1.read()
        
        frame0 = cv2.resize(frame0,(224,224))
        frame1 = cv2.resize(frame1,(224,224))
        
        cv2.imshow("0",frame0)
        cv2.imshow("1",frame1)
        
    
        dist = ultrasonic.distance()
        end = time.time()
        if (end - start > 1): # 0.5 sec
            print(f"{dist:.2f} cm")
            start = end

        if(dist < DIST_THRES):
            time.sleep(2)
            print("Starting prediction")
            pred_value,confidence=cam_predict.cam_predict(classify_lite, frame0, frame1)
            print(f"{class_names[pred_value[0]]} {confidence[0]:.2f} - cam0")
            print(f"{class_names[pred_value[1]]} {confidence[1]:.2f} - cam1")
            print(f"{class_names[pred_value[2]]} {confidence[2]:.2f} - Final")
            # tilt_general()
            time.sleep(3)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
        
        # if inp == 48:
        #     tilt_paper()
        # elif inp == 49:
        #     tilt_plastic()
        # elif inp == 50:
        #     tilt_can()
        # elif inp == 51:
        #     tilt_general()
    
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()
    
if __name__=="__main__":
    main()

# def old_main():
#     classify_lite = cam_predict.init_pred()

#     while True:
#         with picamera.PiCamera() as camera:
#             camera.resolution = (224,224)
#             camera.framerate = 30
#             camera.start_preview()


#             # Create a PiRGBArray to store the frames
#             raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

#         # Allow the camera to warm up
#         time.sleep(2)
#         while True:
#             dist = ultrasonic.distance()
#             print(f"{dist:.1f} cm")
#             time.sleep(1)
            
#             if(dist<100):
#                 break
#         pred_value,confidence=cam_predict.cam_predict_(classify_lite, raw_capture, camera)
#         print(f"{class_names[pred_value]} {confidence:.2f}")