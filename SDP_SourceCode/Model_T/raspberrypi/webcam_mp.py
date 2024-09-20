import cv2
import threading
class_names = ['Can','Paper','Plastic']
def init():
    return 0
def cam_predict2(classify_lite, frame0, frame):
    for i in range(10000):
        if True:
            x = 1
    return 0, 87
class VideoProcessor:
    def __init__(self):
        self.frame = None
        self.classify_lite = init()
        self.lock = threading.Lock()

    def start_video_capture(self):
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
                cv2.imshow('Video', frame)
                cv2.waitKey(1)

    def process_and_save_frame(self):
        while True:
            with self.lock:
                if self.frame is not None:
                    # resized_frame = cv2.resize(self.frame, (self.resize_width, self.resize_height))
                    # cv2.imwrite(self.save_file_path, resized_frame)

                    self.frame = cv2.resize(self.frame, (224,224))
                    pred_value,confidence = cam_predict2(self.classify_lite, None, self.frame)
                    print(f"{class_names[pred_value]} with a(n) {confidence:.2f}% confidence.")
                    self.frame = None



if __name__ == '__main__':
    video_processor = VideoProcessor()

    video_capture_process = threading.Thread(target=video_processor.start_video_capture)
    video_capture_process.start()

    process_and_save_process = threading.Thread(target=video_processor.process_and_save_frame)
    process_and_save_process.start()

    video_capture_process.join()
    process_and_save_process.join()

    cv2.destroyAllWindows()
