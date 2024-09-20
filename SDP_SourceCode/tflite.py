import time
import picamera
import picamera.array
import numpy as np

import tensorflow as tf
import PIL
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import RPi.GPIO as GPIO

# for servo

from adafruit_servokit import ServoKit    #https://circuitpython.readthedocs.io/projects/servokit/en/latest/

# Constants
nbPCAServo=16 

#Parameters
MIN_IMP  =[500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
MAX_IMP  =[2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500, 2500]
MIN_ANG  =[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[360, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]

#Objects
pca = ServoKit(channels=16)

# function init 
# for i in range(nbPCAServo):
    # pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])
pca.servo[0].set_pulse_width_range(MIN_IMP[0] , MAX_IMP[0])

MID = 75
MAX_TILT = 15
pca.servo[0].angle = MID


# Upto this is for servo

GPIO.setwarnings(False)


# YELLOW_LED = 17
# GREEN_LED = 18
# BLUE_LED = 22

#sensor GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 15
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


# GPIO.setmode(GPIO.BCM)

# GPIO.setup(YELLOW_LED, GPIO.OUT)
# GPIO.setup(GREEN_LED, GPIO.OUT)
# GPIO.setup(BLUE_LED, GPIO.OUT)

def distance():
    # # Set trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # # Set trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start_time = time.time()
    stop_time = time.time()
    # Save start time
    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        stop_time = time.time()

    # Time difference between start and arrival
    time_elapsed = stop_time - start_time

    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2

    return distance

class_names = ['Can','Paper','Plastic']

def yellow():
    GPIO.output(17, True) #yellow
    time.sleep(1)
    GPIO.output(17, False) 

def green():
    GPIO.output(18, True)   #green
    time.sleep(1)
    GPIO.output(18, False)

def blue():
    GPIO.output(22, True)   #blue
    time.sleep(1)
    GPIO.output(22, False)

# define a dictionary of functions
switcher = {
    0: yellow,
    1: green,
    2: blue
}

def tilt_left():
    for j in range(MID, MID - MAX_TILT,-1):
        pca.servo[0].angle = j
        time.sleep(0.05)
    time.sleep(1)
    for j in range(MID-MAX_TILT, MID, 1):
        pca.servo[0].angle = j
        time.sleep(0.05)


def tilt_right():
    for j in range(MID,MID + MAX_TILT,1):
        pca.servo[0].angle = j
        time.sleep(0.05)
    time.sleep(1)

    for j in range(MID + MAX_TILT, MID,-1):
        pca.servo[0].angle = j
        time.sleep(0.05)

def not_yet():
    print("NOT YET IMPLEMENTED")

def cam_predict():
    
    TF_MODEL_FILE_PATH = 'VGG16-STBv1.2Lite' # The default path to the saved TensorFlow Lite model

    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

    interpreter.get_signature_list()

    classify_lite = interpreter.get_signature_runner('serving_default')

    with picamera.PiCamera() as camera:
        camera.resolution = (224,224)
        camera.framerate = 30
        camera.start_preview()

        # Create a PiRGBArray to store the frames
        raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

        # Allow the camera to warm up
        time.sleep(2)

        # Capture video frames into the PiRGBArray
        for _ in camera.capture_continuous(raw_capture, format='rgb', use_video_port=True):
            # Get the numpy array of the frame
            frame = raw_capture.array
            print("here")    
            img_array = tf.expand_dims(frame, axis=0)
            print("here1")    

            img_array = tf.cast(img_array, tf.float32)


                # time.sleep(2)
            predictions_lite = classify_lite(input_4=img_array)['dense_5']
            score_lite = tf.nn.softmax(predictions_lite)
                
            pred_value = np.argmax(score_lite)
                
            # switcher.get(pred_value, lambda: print("Invalid key"))()
            servo_switcher.get(pred_value, lambda: print("Invalid key"))()
                

            print(
                "This image most likely belongs to {} with a {:.2f} percent confidence."
                .format(class_names[pred_value], 100 * np.max(score_lite))
            )
                # exit(0)
                # Clear the PiRGBArray in preparation for the next frame
            raw_capture.truncate(0)

            # # Stop capturing frames after 10 seconds
            # if time.time() - start_time > 10:
            break

        # Stop the preview
        #camera.stop_preview()
        
    # '''


servo_switcher = {
    0: not_yet,
    1: tilt_left,
    2: tilt_right
}

while True:
    while True:
            dist = distance()
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if(dist<100):
                break

    pred=cam_predict()


    # TF_MODEL_FILE_PATH = '/home/stb/Downloads/VGG16-STBv1.2Lite' # The default path to the saved TensorFlow Lite model

    # interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

    # interpreter.get_signature_list()

    # classify_lite = interpreter.get_signature_runner('serving_default')

    # cam_predict()

    
    # with picamera.PiCamera() as camera:
    #     camera.resolution = (224,224)
    #     camera.framerate = 30
    #     camera.start_preview()

    #     # Create a PiRGBArray to store the frames
    #     raw_capture = picamera.array.PiRGBArray(camera, size=camera.resolution)

    #     # Allow the camera to warm up
    #     time.sleep(2)

    #     # Capture video frames into the PiRGBArray
    #     for _ in camera.capture_continuous(raw_capture, format='rgb', use_video_port=True):
    #         # Get the numpy array of the frame
    #         frame = raw_capture.array
            
    #         img_array = tf.expand_dims(frame, axis=0)
    #         img_array = tf.cast(img_array, tf.float32)


    #         # time.sleep(2)
    #         predictions_lite = classify_lite(input_4=img_array)['dense_5']
    #         score_lite = tf.nn.softmax(predictions_lite)
            
    #         pred_value = np.argmax(score_lite)
            
    #         # switcher.get(pred_value, lambda: print("Invalid key"))()
    #         servo_switcher.get(pred_value, lambda: print("Invalid key"))()
            

    #         print(
    #             "This image most likely belongs to {} with a {:.2f} percent confidence."
    #             .format(class_names[pred_value], 100 * np.max(score_lite))
    #         )
    #         # exit(0)
    #         # Clear the PiRGBArray in preparation for the next frame
    #         raw_capture.truncate(0)

    #         # # Stop capturing frames after 10 seconds
    #         # if time.time() - start_time > 10:
    #         break

    #     # Stop the preview
    #     camera.stop_preview()
        
   


