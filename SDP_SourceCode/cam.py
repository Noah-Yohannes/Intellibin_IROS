import time
import picamera
import picamera.array

# Set up the camera
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
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

        
        
        # Print the dimensions of the frame
        print(frame.shape)

        # Clear the PiRGBArray in preparation for the next frame
        raw_capture.truncate(0)

        # # Stop capturing frames after 10 seconds
        # if time.time() - start_time > 10:
        #     break

    # Stop the preview
    camera.stop_preview()
