from datetime import timedelta
import cv2
import numpy as np
import os

SAVING_FRAMES_PER_SECOND = 25


def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """A function that returns the list of durations where to save the frames"""
    s = []
    # get the clip duration by dividing number of frames by the number of frames per second
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / \
        cap.get(cv2.CAP_PROP_FPS)
    # use np.arange() to make floating-point steps
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def find_w_h(w, h):
    sq = min(w, h)
    hc, wc = h / 2, w / 2
    x = wc - sq / 2
    y = hc - sq / 2

    return (int(x), int(y), int(sq), int(sq))


def main(video_file, video_file_):
    filename, _ = os.path.splitext(video_file_)

    # make a folder by the name of the video file
    if not os.path.isdir(filename):
        os.mkdir(filename)

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    saving_frames_durations = get_saving_frames_durations(
        cap, saving_frames_per_second)

    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if (w != h):
        print(f"{video_file} will be cropped")
    (x, y, w, h) = (0, 0, int(w), int(h)) if w == h else find_w_h(w, h)

    # print(x,y,w,h)
    count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            break
        # get the duration by dividing the frame count by the FPS
        frame_duration = count / fps
        try:
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # the list is empty, all duration frames were saved
            break
        if frame_duration >= closest_duration:
            # if closest duration is less than or equals the frame duration,
            # then save the frame
            frame_duration_formatted = format_timedelta(
                timedelta(seconds=frame_duration))
            cv2.imwrite(os.path.join(
                filename, f"{frame_duration_formatted}.png"), frame[y:y+h, x:x+w])
            # drop the duration spot from the list, since this duration spot is already saved
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # increment the frame count
        count += 1


if __name__ == "__main__":
    import sys
    next = True
    videos = []

    directory = input(
        "Path of directory: inside it should be videos only (So expecting name of one of the classes): ")
    new_directory = f"{directory}_"

    # iterate over files in that directory
    from tqdm import tqdm
    for filename in tqdm(os.listdir(directory)):
        f = os.path.join(directory, filename)
        f_ = os.path.join(new_directory, filename)

        if not os.path.isdir(new_directory):
            os.mkdir(new_directory)

        main(f, f_)

    # for i in range(len(videos)):
