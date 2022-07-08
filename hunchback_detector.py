"""
Detect hunchback with face detection
"""
from threading import Thread
import tempfile
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


def label_object(location: tuple, text: str, shrink: float, frame: np.ndarray):
    """
    label the object on th frame
    """
    area = calculate_area(location)
    if area > 9756 * 0.9:
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


def trigger_warning(locations: list, noface: int, noface_conti: int,
                    limit: int) -> tuple:
    """
    Determine if the face cannot be detected and trigger a warning
    """
    if len(locations) == 0:
        noface += 1
    elif len(locations) == 1:
        area = calculate_area(locations[0])
        if area < 9756 * 0.9:
            noface += 1
        else:
            noface = noface_conti = 0
    else:
        noface = noface_conti = 0

    if noface >= limit and noface_conti < 3:
        thre = Thread(target=warning, args=["抬頭挺胸", "zh-tw"])
        thre.start()
        noface = 0
        noface_conti += 1
    return (noface, noface_conti)


def show_webcam(shrink: float = 0.25,
                detect_every_n_frames: int = 5,
                show: bool = False,
                camera: int = 1,
                fhp_second: int = 60) -> None:
    """
    Show webcam
    """
    cam = cv2.VideoCapture(camera)
    noface = 0
    noface_conti = 0
    frame_count = 0
    ret_val = True
    while ret_val:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        shape = frame.shape
        small_frame = cv2.resize(frame, (0, 0), fx=shrink, fy=shrink)
        if frame_count % detect_every_n_frames == 0:
            locations = face_locations(small_frame)
            limit = fhp_second * (30 // detect_every_n_frames)
            noface, noface_conti = trigger_warning(locations, noface,
                                                   noface_conti, limit)
            if show:
                for location in locations:
                    label_object(location, "face", shrink, frame)
                cv2.putText(frame, "Press ESC to quit", (40, 40), 0,
                            1e-3 * shape[0], (0, 0, 255),
                            int((shape[0] + shape[1]) // 900))
                cv2.imshow('web stream', frame)

        esc_key = cv2.waitKey(1)
        if esc_key == 27:
            break  # esc to quit

        frame_count += 1

    cv2.destroyAllWindows()


@click.command()
@click.option('--show', is_flag=True, default=False, help="show the video")
@click.option('--camera', default=0, help="choose camera")
@click.option('--fhps',
              default=10,
              help="Maximum Forward Head Posture duration (seconds)")
def main(show, camera, fhps):
    """
    start the program
    """
    show_webcam(show=show, camera=camera, fhp_second=fhps)


# pylint: disable=no-value-for-parameter
if __name__ == '__main__':
    main()
