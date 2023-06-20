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
    else:
        python_script = open(f'scripts/{file_name}.py', 'w')

    python_script.write("import time\n")
    python_script.write("import pyautogui, os\n")
    python_script.write("from PIL import Image\n")
    python_script.write("import requests\n")
    python_script.write("import json\n\n")

    python_script.write("def run_script():\n")

    steps = script.splitlines()
    json_data = ''

    if "Get API" in steps[0]:
        url = steps[0].split('|')[4]
        json_data = request_get(url)
        python_script.write(f"  json_data = request_get({url})\n\n")
        steps.pop(0)

    for step in steps:
        image_x_y_action = step.split('|')
        image_found = False


    python_script.write("def request_get(url):\n")
    python_script.write("   try:\n")
    python_script.write("       response = requests.get(url)\n")
    python_script.write("       response.raise_for_status()\n")
    python_script.write("       json_data = response.json()\n")
    python_script.write("       return json_data\n")
    python_script.write("   except requests.exceptions.RequestException as e:\n")
    python_script.write("       print(\"Error\", e)\n\n")

    python_script.write("if __name__ == \'__main__\':\n")
    python_script.write("   run_script()\n\n")

    # python_script.write("\n")

def request_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print("Error", e)