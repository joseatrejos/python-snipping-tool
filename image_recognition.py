import time
import pyautogui, os
from PIL import Image
import requests
import json

def run_script(script, iteration):
    steps = script.splitlines()
    json_data = ''

    if "Get API" in steps[0]:
        url = steps[0].split('|')[4]
        json_data = request_get(url)
        steps.pop(0)

    for step in steps:
        image_x_y_action = step.split('|')
        image_found = False

        time_iteration = time.time()

        while not image_found:
            image = Image.open(image_x_y_action[0])
            location = pyautogui.locateOnScreen(image)

            actual_time = time.time()
            if actual_time - time_iteration >= 15:
                return True
            
            if location is not None:
                x = location.left + int(image_x_y_action[1])
                y = location.top + int(image_x_y_action[2])

                action = image_x_y_action[3]
                pyautogui.moveTo(x, y, duration=1)
                time.sleep(.5)

                if action == 'Right click':
                    pyautogui.click()
                elif action == 'Double click':
                    pyautogui.doubleClick()
                elif action == 'Text':
                    pyautogui.click()
                    pyautogui.typewrite(image_x_y_action[4])
                    pyautogui.press('enter')
                elif action == "From Json":
                    pyautogui.click()
                    
                    if iteration <= len(json_data):
                        sale = json_data[iteration]
                        
                        json_key = image_x_y_action[4]
                        keys = json_key.split('-')
                        for key in keys:
                            if len(sale) == 0:
                                break
                            sale = sale[key]

                        pyautogui.click()
                        pyautogui.typewrite(str(sale))
                        pyautogui.press('enter')    

                image_found = True

def request_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print("Error", e)