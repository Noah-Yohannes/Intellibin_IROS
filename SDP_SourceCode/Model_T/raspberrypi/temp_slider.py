import tkinter as tk
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2
import numpy as np
from tensorflow import keras
import os

MODEL_PATH = "Models\ResNet50-STBv1.0_17"

model = keras.models.load_model(MODEL_PATH)


# Create list of image paths and corresponding preds arrays
image_list = []
for filename in os.listdir("testing"):
    if filename.endswith(".png") :
        image_list.append((os.path.join("testing", filename), None))
del filename

def safe_logit(p, eps=1e-6):
    # Clip p to a small range around 0 or 1
    p = tf.clip_by_value(p, eps, 1-eps)
    # Compute the logit using the clipped probability value
    logit = tf.math.log(p / (1 - p))
    return logit

for i, (image_path, _) in enumerate(image_list):
    # Load image and resize
    print(image_path)
    test_img = plt.imread(image_path)
    if test_img.shape[-1] == 4:
        test_img = test_img[:, :, :-1]
    test_img = cv2.resize(test_img,(224,224))
    img_array = tf.expand_dims(test_img, axis=0) 
    img_array = tf.cast(img_array, tf.float32)
    
    # Get predictions for image
    preds = model.predict(img_array*255.0)
    preds = safe_logit(preds) # inverse of sigmoid function
    print(preds)
    image_list[i] = (image_path, preds)



# Define custom activation function with temperature scaling
def scaled_softmax(x, temperature=1.0):
    # sm_wz_temp = np.exp(x/temperature) / np.sum(np.exp(x/temperature), axis=0)
    # softmax_output = tf.keras.activations.softmax(x / temperature)
    # x /= np.max(x)
    # return sm_wz_temp
    return tf.nn.softmax(x / temperature)
    # return x/temperature
    # return tf.math.tanh(x / temperature)

# Create GUI with slider and output labels
output_labels = [None]*len(image_list)

root = tk.Tk()
root.title("Scaled Softmax Slider")

temperature_label = tk.Label(root, text="Temperature: 0.0")
temperature_label.pack()

def update_temperature(value):
    temperature = float(value)/1.0
    temperature_label.config(text=f"Temperature: {temperature}")
    
    for i, (image_path, preds) in enumerate(image_list):
        if preds is None:
            continue
        scaled = scaled_softmax(preds, temperature)[0]

        # remove all others except the max
        # scaled = [0 if val != max(scaled) else val for val in scaled]
        out = ' '.join([f'{0 if val != max(scaled) else val*100}' for val in scaled])
        output_labels[i].config(text=f"{os.path.basename(image_path)} {out}")


temperature_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=update_temperature)


temperature_slider.set(10)
temperature_slider.pack()

for i, (image_path, preds) in enumerate(image_list):
    if preds is None:
        continue
    output_label = tk.Label(root, text=os.path.basename(image_path) + " " + "0.00 0.00 0.00")
    output_label.pack()
    output_labels[i] = output_label


root.mainloop()