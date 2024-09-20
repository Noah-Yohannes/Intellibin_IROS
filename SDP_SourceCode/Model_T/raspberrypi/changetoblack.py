import cv2
import numpy as np

def change_background_to_black(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply a threshold to create a binary mask separating the foreground from the background
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # Find the contours of the foreground object
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a black background image of the same size as the input image
    background = np.zeros_like(image)
    
    # Draw the contours of the foreground object on the black background
    cv2.drawContours(background, contours, -1, (0, 0, 0), thickness=cv2.FILLED)
    
    # Combine the black background with the foreground object
    result = cv2.bitwise_and(image, background)
    
    # Save or display the resulting image
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Provide the path to the input image
image_path = 'testing\general_143.PNG'

# Call the function to change the background to black
# change_background_to_black(image_path)
# opencv loads the image in BGR, convert it to RGB
img = cv2.cvtColor(cv2.imread(image_path),
                   cv2.COLOR_BGR2RGB)
lower_white = np.array([220, 220, 220], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)
mask = cv2.inRange(img, lower_white, upper_white)  # could also use threshold
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # "erase" the small white points in the resulting mask
mask = cv2.bitwise_not(mask)  # invert mask

# load background (could be an image too)
bk = np.full(img.shape, 255, dtype=np.uint8)  # white bk

# get masked foreground
fg_masked = cv2.bitwise_and(img, img, mask=mask)

# get masked background, mask must be inverted 
mask = cv2.bitwise_not(mask)
bk_masked = cv2.bitwise_and(bk, bk, mask=mask)

# combine masked foreground and masked background 
final = cv2.bitwise_or(fg_masked, bk_masked)
mask = cv2.bitwise_not(mask)  # revert mask to original
res = cv2.bitwise_not(img, img, mask)
cv2.imshow('res', res) # gives black background
cv2.waitKey(0)
cv2.destroyAllWindows()