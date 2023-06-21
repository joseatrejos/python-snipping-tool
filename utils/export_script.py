import subprocess
import time
import pyautogui, os
from PIL import Image
import requests

def export_script(script, file_name):
    
    # Create a file .py
    i = 0
    if os.path.isfile(f'scripts/{file_name}.py'):
        while os.path.isfile(f'scripts/{file_name}{i}.py'):
            i += 1
        # if file_name already exist add a number
        python_script = open(f'scripts/{file_name}{i}.py', 'w')
        file_path = f'scripts/{file_name}{i}.py'
    else:
        python_script = open(f'scripts/{file_name}.py', 'w')
        file_path = f'scripts/{file_name}.py'

    python_script.write("import time\n")
    python_script.write("import pyautogui, os\n")
    python_script.write("from PIL import Image\n")
    python_script.write("import requests\n")
    python_script.write("import keyboard\n")
    python_script.write("import json\n\n")

    python_script.write("def run_script():\n")

    steps = script.splitlines()

    if "Get API" in steps[0]:
        url = steps[0].split('|')[4]
        python_script.write(f"    json_data = request_get(\'{url}\')\n\n")
        steps.pop(0)

        python_script.write("    for object in json_data:\n\n")
        
        for i, step in enumerate(steps):
            python_script.write(f"        # Start step #{i}\n")
            
            image_x_y_action = step.split('|')

            python_script.write("        image_found = False\n")
            python_script.write("        while not image_found:\n")
            python_script.write(f"            image = Image.open(\'./{image_x_y_action[0]}\')\n")
            python_script.write("            location = pyautogui.locateOnScreen(image)\n")
            python_script.write("            if location is not None:\n")
            python_script.write(f"                x = location.left + int(\'{image_x_y_action[1]}\')\n")
            python_script.write(f"                y = location.top + int(\'{image_x_y_action[2]}\')\n")
            python_script.write("                pyautogui.moveTo(x, y, duration = 1)\n")
            python_script.write("                time.sleep(.5)\n")
            
            action = image_x_y_action[3]
            if action == 'Right click':
                python_script.write("                pyautogui.click()\n")
            elif action == 'Double click':
                python_script.write("                pyautogui.doubleClick()\n")
            elif action == 'Text':
                python_script.write("                pyautogui.click()\n")
                python_script.write(f"                pyautogui.typewrite(\'{image_x_y_action[4]}\')\n")
                python_script.write("                pyautogui.press(\'enter\')\n")
            elif action == 'Delete':
                python_script.write("                pyautogui.click()\n")
                python_script.write("                pyautogui.press(\'backspace\')\n")
                python_script.write("                pyautogui.press(\'enter\')\n")
            elif action == "From Json":
                python_script.write(f"                value = find_key_value(object, \'{image_x_y_action[4]}\')\n")
                python_script.write("                pyautogui.doubleClick()\n")
                python_script.write("                pyautogui.typewrite(str(value))\n")
                python_script.write("                pyautogui.press('enter')\n")

            python_script.write("            image_found = True\n")
            python_script.write(f"        # End step #{i}\n\n")

    else:
        for i, step in enumerate(steps):
            python_script.write(f"    # Start step #{i}\n")
            
            image_x_y_action = step.split('|')

            python_script.write("    image_found = False\n")
            python_script.write("    while not image_found:\n")
            python_script.write(f"        image = Image.open(\'./{image_x_y_action[0]}\')\n")
            python_script.write("        location = pyautogui.locateOnScreen(image)\n")
            python_script.write("        if location is not None:\n")
            python_script.write(f"            x = location.left + int(\'{image_x_y_action[1]}\')\n")
            python_script.write(f"            y = location.top + int(\'{image_x_y_action[2]}\')\n")
            python_script.write("            pyautogui.moveTo(x, y, duration = 1)\n")
            python_script.write("            time.sleep(.5)\n")
            
            action = image_x_y_action[3]
            if action == 'Click':
                python_script.write("            pyautogui.click()\n")
            elif action == 'Double click':
                python_script.write("            pyautogui.doubleClick()\n")
            elif action == 'Text':
                python_script.write("            pyautogui.click()\n")
                python_script.write(f"            pyautogui.typewrite(\'{image_x_y_action[4]}\')\n")
                python_script.write("            pyautogui.press(\'enter\')\n")
            elif action == 'Delete':
                python_script.write("            pyautogui.click()\n")
                python_script.write("            pyautogui.press(\'backspace\')\n")
                python_script.write("            pyautogui.press(\'enter\')\n")
            elif action == "From Json":
                python_script.write(f"            value = find_key_value(object, \'{image_x_y_action[4]}\')\n")
                python_script.write("            pyautogui.doubleClick()\n")
                python_script.write("            pyautogui.typewrite(str(value))\n")
                python_script.write("            pyautogui.press(\'enter\')\n")

            python_script.write("        image_found = True\n")
            python_script.write(f"    # End step #{i}\n\n")


    python_script.write("def request_get(url):\n")
    python_script.write("    try:\n")
    python_script.write("        response = requests.get(url)\n")
    python_script.write("        response.raise_for_status()\n")
    python_script.write("        json_data = response.json()\n")
    python_script.write("        return json_data\n")
    python_script.write("    except requests.exceptions.RequestException as e:\n")
    python_script.write("        print(\"Error\", e)\n\n")

    python_script.write("def find_key_value(json_data, json_keys):\n")
    python_script.write("    keys = json_keys.split(\'-\')\n")
    python_script.write("    for key in keys:\n")
    python_script.write("        if len(json_data) == 0:\n")
    python_script.write("            break\n")
    python_script.write("        json_data = json_data[key]\n")
    python_script.write("    return json_data\n\n")

    python_script.write("if __name__ == \'__main__\':\n")
    python_script.write("    run_script()\n\n")
    python_script.write("# If you want to make it an infinite loop\n")
    python_script.write("# comment the last line and uncomment the next code\n\n")
    python_script.write("#     stop_iteration = False\n\n")
    python_script.write("#     def stop_infinite_loop(e):\n")
    python_script.write("#         global stop_iteration\n")
    python_script.write("#         if e.name == \'q\' and e.event_type == \'down\' and keyboard.is_pressed(\'ctrl\'): \n")
    python_script.write("#             stop_iteration = True\n\n")
    python_script.write("#     keyboard.on_press(stop_infinite_loop)\n\n")
    python_script.write("#     while not stop_iteration:\n")
    python_script.write("#         run_script()\n\n")
    python_script.write("#     keyboard.unhook_all()\n")
    python_script.close()

    return file_path

    # python_script.write("\n")