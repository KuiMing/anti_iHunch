"""
GUI for Forward Head Position Alert
"""
import os
import sys
import tkinter as tk
from tkinter import ttk
import cv2
from hunchback_detector import FHPDetection

# pylint: disable=maybe-no-member


def detect_face(small_frame):
    """
    Detect face
    """
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.dirname(__file__)
    face_detector = cv2.CascadeClassifier(
        os.path.join(path, "haarcascade_frontalface_default.xml"))
    faces = face_detector.detectMultiScale(small_frame, minSize=(50, 50))
    locations = []
    for i in faces:
        left, top, width, height = i
        locations.append([top, left + width, top + height, left])
    return locations


class Application(ttk.Frame):
    """
    Anti FHP application
    """
    def __init__(self, master):

        if getattr(sys, 'frozen', False):
            path = os.path.dirname(sys.executable)
        elif __file__:
            path = os.path.dirname(__file__)

        self.config_file = os.path.join(path, "config.json")
        self.fhp_detector = FHPDetection(show=True,
                                         face_detector=detect_face,
                                         config_file=self.config_file)

        ttk.Frame.__init__(self, master)
        self.pack()
        self.button_detect = ttk.Button(self, width=20)
        self.button_detect["text"] = "Setting"
        self.button_detect["command"] = self.setting
        self.button_detect.pack(side="top", padx=10, pady=10)
        self.button_setting = ttk.Button(self, width=20)
        self.button_setting["text"] = "Detect FHP"
        self.button_setting["command"] = self.detect
        self.button_setting.pack(side="top", padx=10, pady=10)

    def setting(self):
        """
        Detection Setting
        """
        self.fhp_detector.set_configure()
        self.fhp_detector.start_detection()

    def detect(self):
        """
        Detection function
        """
        if not os.path.isfile(self.config_file):
            print("setting mode")
            self.fhp_detector.set_configure()
        self.fhp_detector.start_detection()


def main():
    """
    GUI for Forward Head Position Alert
    """
    root = tk.Tk()
    root.title("Anti-FHP")
    window_width = 250
    window_height = 90
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root['background'] = "#E9E9E9"
    Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
