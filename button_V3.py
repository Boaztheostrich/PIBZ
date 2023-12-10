from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from gpiozero import Button
import threading
import os

picam2 = Picamera2()
button = Button(16)
camera_config = picam2.create_preview_configuration(main={"size": (4056, 3040)}, lores={"size": (480, 360)}, display="lores", buffer_count=5)
picam2.configure(camera_config)

# Global flag to indicate whether the capture function is in progress
capture_in_progress = False

def capture():
    global capture_in_progress
    with open("picture_count.txt", "r") as file:
        number = int(file.read())

    number += 1

    # Get the home directory of the current user
    home_directory = os.path.expanduser("~")

    # Construct the path to the images directory
    images_directory = os.path.join(home_directory, "Desktop", "images")

    # Ensure the images directory exists, create it if necessary
    os.makedirs(images_directory, exist_ok=True)

    # Capture the image with the updated path
    metadata = picam2.capture_file(os.path.join(images_directory, "pibz_" + str(number) + ".jpg"))

    with open("picture_count.txt", "w") as file:
        file.write(str(number))

    print(metadata)

    # Set the flag to indicate that the capture is complete
    capture_in_progress = False

def button_monitor():
    global capture_in_progress
    while True:
        if not capture_in_progress and button.is_pressed:
            print("Button pressed!")

            # Print the username of the current user
            username = os.path.basename(os.path.expanduser("~"))
            print(f"Current user: {username}")

            # Set the flag to indicate that the capture is in progress
            capture_in_progress = True
            
            # Start the capture function in a new thread
            capture_thread = threading.Thread(target=capture)
            capture_thread.start()

def display_preview():
    picam2.start_preview(Preview.QTGL, width=549, height=412)
    picam2.start()

# Create and start the threads
button_thread = threading.Thread(target=button_monitor)
preview_thread = threading.Thread(target=display_preview)

button_thread.start()
preview_thread.start()

# Wait for the threads to finish (this won't happen since they run indefinitely)
button_thread.join()
preview_thread.join()
