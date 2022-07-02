"""
Detect hunchback with face detection
"""
import os
import cv2
import face_recognition
# pylint: disable=maybe-no-member


def show_webcam():
    """
    show webcam
    """
    cam = cv2.VideoCapture(0)
    process_frame = True
    noface = 0
    noface_conti = 0
    shrink = 0.25
    while True:
        ret_val, frame = cam.read()
        frame = cv2.flip(frame, 1)
        small_frame = cv2.resize(frame, (0, 0), fx=shrink, fy=shrink)
        if ret_val:

            # if process_frame:
            face_locations = face_recognition.face_locations(small_frame)
            if len(face_locations) == 0:
                noface += 1
                # print("no face")
                if noface >= 10 and noface_conti < 3:
                    os.system("say 抬頭挺胸")
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
            process_frame = not process_frame
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
