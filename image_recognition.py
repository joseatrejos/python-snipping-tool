import pyautogui, os
from PIL import Image

def find_images_on_screen(images):

    # Load the target images
    target_images = [Image.open(f"screenshots/{images}") for images in images]

    while True:

        # Start: Reload Images if Debugging
        images = load_images()
        target_images = [Image.open(f"screenshots/{images}") for images in images]
        # End Debugging

        found_image = False

        for index, target_image in enumerate(target_images):
            
            # # How to define a search region for optimization purposes
            # # If you want to define a search region starting from (100, 100) and extending 200 pixels 
            # # to the right and 150 pixels down, you would set search_region as (100, 100, 200, 150). 
            # # This creates a rectangular region of 200 pixels in width and 150 pixels in height, 
            # # starting from 100 pixels of distance from the top and from the left of your screen's
            # # top-left corner.
            # search_region = (100, 100, 800, 600)  # Adjust the coordinates as per your requirement

            # Search for the target image on the screen
            location = pyautogui.locateOnScreen(target_image)

            # If image is found
            if location is not None:
                found_image = True
                print(f"Image {target_image.filename.split('/')[1]} found at location:", location)

        # Check if no images have been found
        if found_image == False:
            print("No Image found. Searching again...")

def load_images():
    return os.listdir('screenshots')

if __name__ == "__main__":

    # Obtain a list of filenames of the photos found in our screenshots folder
    images = load_images()
    find_images_on_screen(images)
