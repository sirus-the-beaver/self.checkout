"""
This script is used to automate the processs of taking a picture of the customer's ID
 with the camera after their ID has been validated as legit (via government API).
"""

import os
from picamera import PiCamera
from time import sleep

save_dir = "./training/person/"
camera = PiCamera()
camera.resolution = (1024, 768)

def capture_image():
    image_name = "id_image.jpg"
    image_path = os.path.join(save_dir, image_name)

    camera.start_preview(alpha=200)
    sleep(5)
    camera.capture(image_path)
    camera.stop_preview()

capture_image()