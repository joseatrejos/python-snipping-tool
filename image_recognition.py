import time
import pyautogui, os
from PIL import Image

def run_script(script):
    steps = script.splitlines()
    for step in steps:
        image_x_y = step.split('|')
        image_found = False

        while not image_found:
            image = Image.open(image_x_y[0])
            location = pyautogui.locateOnScreen(image)
            if location is not None:
                x = location.left + int(image_x_y[1])
                y = location.top + int(image_x_y[2])
                print(f"Moving to: {x},{y} and clicking...")
                pyautogui.moveTo(x, y, duration=3)
                time.sleep(1)
                pyautogui.click()
                image_found = True
