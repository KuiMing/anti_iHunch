"""
Detect hunchback with face detection
"""
import json
import os
from threading import Thread
import tempfile
import time
import cv2
import numpy as np
from face_recognition import face_locations
from gtts import gTTS
from pygame import mixer
import click

# pylint: disable=maybe-no-member


def warning(sentence: str, lang: str) -> None:
    """
    Warning for hunchback
    """
    with tempfile.NamedTemporaryFile(delete=True) as file:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(file.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(file.name))
        mixer.music.play(1)


def label_object(location: tuple, text: str, shrink: float, frame: np.ndarray,
                 face_area: float):
    """
    label the object on th frame
    """
    area = calculate_area(location)
    if area > face_area * 0.9:
        top, right, bottom, left = [int(i / shrink) for i in location]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255),
                      cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, text, (left + 6, bottom - 6), font, 1.0,
                    (255, 255, 255), 1)


def calculate_area(location: tuple):
    """
    Calculate area
    """
    top, right, bottom, left = location
    return (right - left) * (bottom - top)


def trigger_warning(locations: list, fhp_time: float, noface_conti: int,
                    limit: int, face_area: float) -> tuple:
    """
    Determine if the face cannot be detected and trigger a warning
    """
    if len(locations) == fhp_time == 0:
        fhp_time = time.time()
    elif len(locations) == 1:
        area = calculate_area(locations[0])
        if area < face_area * 0.9 and fhp_time == 0:
            fhp_time = time.time()
        elif area >= face_area * 0.9:
            fhp_time = noface_conti = 0
    elif len(locations) > 1:
        fhp_time = noface_conti = 0
    if fhp_time > 0:
        duration = time.time() - fhp_time
        if duration >= limit and noface_conti < 3:
            thre = Thread(target=warning, args=["抬頭挺胸", "zh-tw"])
            thre.start()
            fhp_time = 0
            noface_conti += 1
    return (fhp_time, noface_conti)


def show_label(locations: tuple,
               shrink: float,
               frame: np.ndarray,
               face_area: int,
               text: str = "Press ESC to quit") -> None:
    """
    Show labels on the video
    """
    shape = frame.shape
    for location in locations:
        label_object(location, "face", shrink, frame, face_area)
    cv2.putText(frame, text, (40, 40), 0, 1e-3 * shape[0], (0, 0, 255),
                int((shape[0] + shape[1]) // 900))


def start_detection(shrink: float = 0.25,
                    detect_every_n_frames: int = 5,
                    show: bool = False,
                    camera: int = 1) -> None:
    """
    start to detect face
    """
    cam = cv2.VideoCapture(camera)
    fhp_time = 0
    noface_conti = 0
    frame_count = 0
    ret_val = True
    config = json.load(open("config.json", 'r'))
    while ret_val:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=shrink, fy=shrink)
        if frame_count % detect_every_n_frames == 0:
            locations = face_locations(small_frame)
            fhp_time, noface_conti = trigger_warning(locations, fhp_time,
                                                     noface_conti,
                                                     config["fhp_second"],
                                                     config["face_area"])
            if show:
                show_label(locations, shrink, frame, config["face_area"])
                cv2.imshow('web stream', frame)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit

        frame_count += 1

    cv2.destroyAllWindows()


def set_configure(shrink: float = 0.25,
                  detect_every_n_frames: int = 5,
                  camera: int = 1) -> None:
    """
    Show webcam
    """
    area = []
    cam = cv2.VideoCapture(camera)
    frame_count = 0
    ret_val = True
    lines = [
        "This is only for one user. Please keep your head up. Press Enter to start setting.",
        "Set limitation for Forward Head Posture. Press 1 for 10 sec, 2 for 1 min & 3 for 10 min.",
        "Detect face size. Setting will finish in 3 seconds."
    ]
    text = lines[0]
    while ret_val:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=shrink, fy=shrink)
        if frame_count % detect_every_n_frames == 0:
            locations = face_locations(small_frame)
            show_label(locations, shrink, frame, 1, text)
            wait_key = cv2.waitKey(1)
            if wait_key == 27:
                break  # esc to quit
            if wait_key == 13:
                text = lines[1]

            if text == lines[1]:
                if chr(wait_key & 255) == "1":
                    fhp_second = 10
                elif chr(wait_key & 255) == "2":
                    fhp_second = 60
                elif chr(wait_key & 255) == "3":
                    fhp_second = 600
                if chr(wait_key & 255) in ["1", "2", "3"]:
                    text = lines[2]
                    count_down = 12
            if text == lines[2]:
                area.append(calculate_area(location=locations[0]))
                count_down -= 1
                cv2.putText(frame, str(count_down // 4 + 1), (40, 200), 0,
                            5e-3 * frame.shape[0], (0, 0, 255),
                            int((frame.shape[0] + frame.shape[1]) // 900))

                if count_down == 0:
                    break
            cv2.imshow('web stream', frame)
        frame_count += 1
    cv2.destroyAllWindows()
    json.dump({
        "face_area": int(np.mean(area)),
        "fhp_second": fhp_second
    }, open("config.json", "w"))


@click.command()
@click.option('--show', is_flag=True, default=False, help="show the video")
@click.option('--camera', default=0, help="choose camera")
@click.option('--setting', is_flag=True, default=False, help="set configure")
def main(show, camera, setting):
    """
    start the program
    """
    if not os.path.isfile("config.json") or setting:
        print("setting mode")
        set_configure(0.25, 5, camera=camera)
        show = True
    start_detection(show=show, camera=camera)


# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    main()
