from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from gpiozero import Button
from signal import pause
picam2 = Picamera2()
button = Button(16)
camera_config = picam2.create_preview_configuration(main={"size": (4056, 3040)}, lores={"size": (480, 360)}, display="lores", buffer_count=5)
picam2.configure(camera_config)

# test edit

def capture():
    with open("picture_count.txt", "r") as file:
        number = int(file.read())

    number += 1

    metadata = picam2.capture_file("/home/boaz/Desktop/images/" + "pibz_" + str(number) +".jpg")

    with open("picture_count.txt", "w") as file:
        file.write(str(number))

    print(metadata)

picam2.start_preview(Preview.QTGL, width=549, height=412)
picam2.start()

while True:
    button.when_pressed = capture
