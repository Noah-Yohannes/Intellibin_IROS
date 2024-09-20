import cv2
import os
import numpy as np

def augment_images(folder_path, output_path, num_augmentations):
    for root, _, files in os.walk(folder_path):
        for file in files:
            image_path = os.path.join(root, file)
            image = cv2.imread(image_path)

            # Generate augmented images
            for i in range(num_augmentations):
                rotate_flag = np.random.choice([cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180])

                rotated_image = cv2.rotate(image, rotate_flag)

                # Resize the image randomly within a certain range
                scale_factor = np.random.uniform(0.8, 1.2)  # Random scale factor between 0.8 and 1.2
                width = int(rotated_image.shape[1] * scale_factor)
                height = int(rotated_image.shape[0] * scale_factor)
                resized_image = cv2.resize(rotated_image, (width, height))

                # Apply a random brightness adjustment
                brightness = np.random.uniform(0.5, 1.5)  # Random brightness between 0.5 and 1.5
                adjusted_image = cv2.convertScaleAbs(resized_image, alpha=brightness)

                # Apply a random rotation
                rotation = np.random.uniform(-60, 80)  # Random rotation between -10 and 10 degrees
                M = cv2.getRotationMatrix2D((adjusted_image.shape[1] / 2, adjusted_image.shape[0] / 2), rotation, 1)
                rotated_final_image = cv2.warpAffine(adjusted_image, M, (adjusted_image.shape[1], adjusted_image.shape[0]))
                
                # Apply a random flip in the x direction
                flip_x = np.random.choice([True, False])  # Randomly decide whether to flip or not
                flipped_x_image = cv2.flip(rotated_final_image, 0 if flip_x else 1)

                # Apply a random flip in the y direction
                flip_y = np.random.choice([True, False])  # Randomly decide whether to flip or not
                flipped_image = cv2.flip(flipped_x_image, 1 if flip_y else 0)

                # Apply a black background
                black_background = np.zeros_like(flipped_image)

                # Combine the rotated image with the black background
                final_image = cv2.addWeighted(black_background, 1.0, flipped_image, 1.0, 0)

                # Save the augmented image
                output_file = f"{image_path}_{i}.png"
                cv2.imwrite(output_file, final_image)

# Specify the folder paths and output path
folder_path = "real-0"
output_path = "augmented_images"

# Specify the number of augmentations per image
num_augmentations = 10

# Create the output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Augment the images
augment_images(folder_path, output_path, num_augmentations)
