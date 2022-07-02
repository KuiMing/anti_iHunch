"""
Detect hunchback with face detection
"""
from threading import Thread
import tempfile
import cv2
from face_recognition import face_locations
from gtts import gTTS
from pygame import mixer


# pylint: disable=maybe-no-member
def warning(sentence, lang):
    with tempfile.NamedTemporaryFile(delete=True) as file:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(file.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(file.name))
        mixer.music.play(1)


def show_webcam(shrink: float = 0.25, detect_every_n_frames: int = 5) -> None:
    """
    show webcam
    """
    cam = cv2.VideoCapture(0)
    noface = 0
    noface_conti = 0
    frame_count = 0
    ret_val = True
    while ret_val:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=shrink, fy=shrink)
        if frame_count % detect_every_n_frames == 0:
            locations = face_locations(small_frame)
            if len(locations) == 0:
                noface += 1
                if noface >= 10 and noface_conti < 3:
                    thre = Thread(target=warning, args=["抬頭挺胸", "zh-tw"])
                    thre.start()
                    noface = 0
                    noface_conti += 1
            else:
                noface = 0
                noface_conti = 0

            for location in locations:
                top, right, bottom, left = [int(i / shrink) for i in location]

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),
                              2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom),
                              (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "face", (left + 6, bottom - 6), font, 1.0,
                            (255, 255, 255), 1)
            cv2.imshow('web stream', frame)

        esc_key = cv2.waitKey(1)

        if esc_key == 27:
            break  # esc to quit
        frame_count += 1

    cv2.destroyAllWindows()


def main():
    """
    start program
    """
    show_webcam()


if __name__ == '__main__':
    main()
