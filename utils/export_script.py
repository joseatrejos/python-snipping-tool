import time
import pyautogui, os
from PIL import Image

def export_script(script, file_name):
    
    i = 0
    if os.path.isfile(f'scripts/{file_name}.py'):
        while os.path.isfile(f'scripts/{file_name}{i}.py'):
            i += 1
        open(f'scripts/{file_name}{i}.py', 'w')
    else:
        open(f'scripts/{file_name}.py', 'w')