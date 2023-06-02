import pyautogui, os
from PIL import Image

def find_images_on_screen(images):

    # Load the target images
    target_images = [Image.open(f"screenshots/{images}") for images in images]

    while True:

        # Reload Images if Debugging
        images = load_images()
        # Load the target images
        target_images = [Image.open(f"screenshots/{images}") for images in images]

        # Capture the screen
        screen_image = pyautogui.screenshot()
        found_image = False

        for index, target_image in enumerate(target_images):

            # Search for the target image on the screen
            location = pyautogui.locate(target_image, screen_image, grayscale=True)

            # If image is found
            if location is not None:
                found_image = True
                print(f"Image {index} found at location:", location)

        # Check if no images have been found
        if found_image == False:
            print("No Image found. Searching again...")

def load_images():
    return os.listdir('screenshots')

if __name__ == "__main__":

    # Obtain a list of filenames of the photos found in our screenshots folder
    images = load_images()
    find_images_on_screen(images)
