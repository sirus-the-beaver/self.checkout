"""
This script is used to automate the processs of taking a picture of the customer's ID
 with the camera after their ID has been validated as legit (via government API).
"""

import os
from picamera import PiCamera
import keyboard

# Set the directory to save the picture to
save_dir = "../training/person"

# Set the camera object
camera = PiCamera()

# Set the camera resolution
camera.resolution = (1024, 768)

# Set the camera rotation
camera.rotation = 180

# Capture the image
def capture_image():
    image_name = "id_image.jpg"
    image_path = os.path.join(save_dir, image_name)
    # Camera warm-up time
    sleep(2)
    camera.capture(image_path)

    # Capture image after barcode is scanned
    keyboard.add_hotkey('ctrl+alt+s', capture_image)

    # Keep the script running
    keyboard.wait('esc')

# Run the script
capture_image()