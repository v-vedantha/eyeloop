import time

import cv2
import numpy as np

import sys
sys.path.append('/Users/vedantha/Desktop/camera-calibration')
import coordinate_mapping
import world_camera
from pynput import mouse
import pyautogui
import time
from pynput import keyboard
from pynput.mouse import Listener, Controller


class custom_Extractor:
    def __init__(self, screen_w=4000, screen_h=3000, camera_w=1000, camera_h=1000, buffer=None):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.camera_w = camera_w
        self.camera_h = camera_h
        self.world_detector = world_camera.compute_world_cam
        self.predictor = coordinate_mapping.Predictor(screen_w, screen_h, camera_w, camera_h)
        
        Listener(on_click=self.on_click).start()
        #self.kl.start()

        self.most_recent_pupil = None
        self.buffer = buffer


    def on_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.left:
                print("Training")
                print(x, y)
                output_point = coordinate_mapping.Point(x, y)
                input = self.get_input()
                if input is None:
                    return
                self.predictor.add_calibration_point(input, output_point)
            else:
                print("Moving")
                self.on_press(keyboard.Key.esc)

    def on_press(self, key):
        if key != keyboard.Key.esc:
            return
        input = self.get_input()
        if input is None:
            return
        output = self.predictor(input)
        print(output)
        #pyautogui.moveTo(output.x, output.y, duration=1)
        #print(output)
        Controller().position = (output.x, output.y)
    
    def get_input(self):
        if self.buffer is not None:
            current_input = coordinate_mapping.Input(buffer=self.buffer)
            if current_input.initialized == False:
                return None
            return current_input
        if self.most_recent_pupil is None:
            return None
    
    def fetch(self, core):
        #print(core.dataout)
        if "pupil" not in core.dataout:
            self.most_recent_pupil = None

        else:
            self.most_recent_pupil = coordinate_mapping.Point(core.dataout["pupil"][0][0], core.dataout["pupil"][0][1])

#extractors_add = [custom_Extractor()]
