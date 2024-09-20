import time

import numpy as np
import servo
import tensorflow as tf
import PIL
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2

class_names = ['Can','Paper','Plastic']

servo_switcher = {
    0: servo.tilt_can,
    1: servo.tilt_paper,
    2: servo.tilt_plastic,
    # 3: servo.tilt_general
}

def init_pred ():
    # TF_MODEL_FILE_PATH = 'Models/InceptionV3-STBv1.0_Lite' # The default path to the saved TensorFlow Lite model
    TF_MODEL_FILE_PATH = 'Models/ResNet50-STBv1.0_17_Lite'

    interpreter = tf.lite.Interpreter(model_path=TF_MODEL_FILE_PATH)

    interpreter.get_signature_list()

    classify_lite = interpreter.get_signature_runner('serving_default')

    return classify_lite

def cam_predict(classify_lite,frame0, frame1):
    # last_layer = 'dense_3' # for InceptionV3-STBv1.0_Lite
    last_layer = 'dense_2' # for ResNet50-STBv1.0_17_Lite
    
    pred_value = [0,0]
    conf = [0.0,0.0]
    
    frame0 = cv2.resize(frame0,(224,224))
    img_array0 = tf.expand_dims(frame0, axis=0)
    img_array0 = tf.cast(img_array0, tf.float32)
    predictions_lite = classify_lite(input_2=img_array0)[last_layer]
    
    pred_value[0] = np.argmax(predictions_lite)
    conf[0] = 100 * np.max(predictions_lite)


    # switcher.get(pred_value, lambda: print("Invalid key"))()
    frame1 = cv2.resize(frame1,(224,224))
    img_array1 = tf.expand_dims(frame1, axis=0)
    img_array1 = tf.cast(img_array1, tf.float32)
    predictions_lite = classify_lite(input_2=img_array1)[last_layer]
    
    pred_value[1] = np.argmax(predictions_lite)
    conf[1] = 100 * np.max(predictions_lite)


    #saving both images
    save_frame(pred_value[0], frame0, 0)
    save_frame(pred_value[1], frame1, 1)

    return conflict_resolution(pred_value,conf)
    # return pred_value,conf

def conflict_resolution(pred_value,conf):
    final_conf = np.max(conf)
    final_pred = pred_value[conf.index(final_conf)]

    # servo_switcher.get(final_pred, lambda: print("Invalid key"))()
    servo_switcher.get(final_pred, lambda: print("Invalid key"))()

    
    pred_value = np.append(pred_value, final_pred)
    conf = np.append(conf, final_conf)

    return pred_value,conf
    

# this one uses the picamera (remove the "_" to use it)
def cam_predict_(classify_lite,raw_capture,camera):
    
    # Capture video frames into the PiRGBArray
    for _ in camera.capture_continuous(raw_capture, format='rgb', use_video_port=True):
        # Get the numpy array of the frame
        frame = raw_capture.array
        print("here")    
        img_array = tf.expand_dims(frame, axis=0)
        print("here1")    

        img_array = tf.cast(img_array, tf.float32)

        predictions_lite = classify_lite(input_2=img_array)['dense_3']
        # score_lite = tf.nn.softmax(predictions_lite)
            
        pred_value = np.argmax(predictions_lite)
        # print(pred_value)
            
        # switcher.get(pred_value, lambda: print("Invalid key"))()
        servo_switcher.get(pred_value, lambda: print("Invalid key"))()
        # servo.tilt_paper()

        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(class_names[pred_value], 100 * np.max(predictions_lite))
        )
            # exit(0)
            # Clear the PiRGBArray in preparation for the next frame
        raw_capture.truncate(0)

        # # Stop capturing frames after 10 seconds
        # if time.time() - start_time > 10:
        break
    return pred_value,100 * np.max(predictions_lite)
        # Stop the preview
        #camera.stop_preview()
        
    # '''
from datetime import datetime
def save_frame(pred_value, frame, i):
    if pred_value == 0:
        label= 'can'
    elif pred_value == 1:
        label = 'paper'
    elif pred_value == 2:
        label = 'plastic'
    elif pred_value == 3:
        label = 'general'
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"real/{label}/{now}_{i}.png"
    cv2.imwrite(filename, frame)