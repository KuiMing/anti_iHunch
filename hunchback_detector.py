"""
Detect hunchback with face detection
"""
import os
import cv2
import face_recognition
from threading import Thread
# pylint: disable=maybe-no-member


def warning():
    os.system("say 抬頭挺胸")


def show_webcam(shrink=0.25):
    """
    show webcam
    """
    cam = cv2.VideoCapture(0)
    noface = 0
    noface_conti = 0

    while True:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=shrink, fy=shrink)
        if ret_val:
            face_locations = face_recognition.face_locations(small_frame)
            if len(face_locations) == 0:
                noface += 1
                if noface >= 10 and noface_conti < 3:
                    thre = Thread(target=warning)
                    thre.start()
                    noface = 0
                    noface_conti += 1
            else:
                noface = 0
                noface_conti = 0

            for location in face_locations:
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

    cv2.destroyAllWindows()


def main():
    """
    start program
    """
    show_webcam()


if __name__ == '__main__':
    main()
