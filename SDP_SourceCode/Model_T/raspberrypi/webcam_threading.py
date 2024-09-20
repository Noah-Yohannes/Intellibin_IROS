import time
import cv2
import os

import threading

def init():
    return 0
def cam_predict2(classify_lite, frame0, frame):
    for i in range(100):
        pass
    return 0, 87
def process_frame(frame, classify_lite):
    frame = cv2.resize(frame, (224,224))
    pred_value,confidence = cam_predict2(classify_lite, None, frame)
    print(f"{class_names[pred_value]} with a(n) {confidence:.2f}% confidence.")

# define a class for capturing and processing frames in a separate thread
class FrameCaptureThread(threading.Thread):
    def __init__(self, cap):
        threading.Thread.__init__(self)
        self.cap = cap
        self.frame = None
        self.running = True
        self.classify_lite = init()
        self.ret = True

    def run(self):
        print("atiiiiye")
        while self.running:
            # classify_lite = cam_predict.init()
            # ret, frame = self.cap.read()
            # if self.ret:
        # print(self.frame.shape)
        # print(self.classify_lite)    
            process_frame(self.frame, self.classify_lite)
                

    def stop(self):
        self.running = False

class_names = ['Can','Paper','Plastic']

def main2():

    # cam0 = cv2.VideoCapture(0)
    cam1 = cv2.VideoCapture(1)

    # assert cam0.isOpened(), "failed to grab frame0"
    assert cam1.isOpened(), "failed to grab frame1"

    # create a FrameCaptureThread object to capture and process frames
    # frame_thread = FrameCaptureThread(cam1)


    # cv2.namedWindow("0")
    # cv2.namedWindow("1")

    # dim = (224,224)

    # print("here")
    
    # frame_thread = FrameCaptureThread(cam1)
    # frame_thread.classify_lite = cam_predict.init()
    # frame_thread.ret, frame = frame_thread.cap.read()
    # frame_thread.frame = frame
    # frame_thread.start()

    while True:

        # frame_thread.ret, frame = frame_thread.cap.read()
        # frame_thread.frame = frame
        # frame = frame_thread.frame
        # frame = cv2.resize(frame,(224,224))
        # display the processed frame
        _, frame = cam1.read()
        cv2.imshow("1", frame)
        # print("in main thread")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
        # frame_thread.start()

        # frame_thread.join()

    # cam0.release()
    cam1.release()
    print("abzi")
    # stop the FrameCaptureThread object and release the VideoCapture object
    # frame_thread.stop()
    # frame_thread.join()
    cv2.destroyAllWindows()

def main3():
    cam0 = cv2.VideoCapture(0)
    cam1 = cv2.VideoCapture(0)

    assert cam0.isOpened(), "failed to grab frame0"
    assert cam1.isOpened(), "failed to grab frame1"
    
    cv2.namedWindow("0")
    cv2.namedWindow("1")

    while True:
        _, frame0 = cam0.read() 
        _, frame1 = cam1.read()
        
        frame0 = cv2.resize(frame0,(224,224))
        frame1 = cv2.resize(frame1,(224,224))
        cv2.imshow("0", frame0)
        cv2.imshow("1", frame1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()

def main4():
    for i in range(1,4):
        cap = cv2.VideoCapture(i)
        if cap.read()[0]:
            print(f"Webcam {i} found!")
        cap.release()

if __name__ == "__main__":
    main3()