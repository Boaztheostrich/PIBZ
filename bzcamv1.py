
import sys
import select
import time
from gpiozero import Button
from picamera2 import Picamera2, Preview

# Button is connected to GPIO 16

button = Button(16)

# Initialize the camera and preview outside the loop
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (4056, 3040)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()

while True:
    # Loop to wait on request
    request = "none"

    while True:
        if button.is_pressed:
            request = "capture"
            break

        key_input = select.select([sys.stdin], [], [], 1)[0]

        if key_input:
            key_value = sys.stdin.readline().rstrip()

            if key_value == "q":
                request = "quit"
                break
            else:
                request = "capture"
                break

    if request == "quit":
        break

    # Capture the image
    metadata = picam2.capture_file("/home/boaz/Desktop/images/" + time.strftime("%Y%m%d-%H%M%S") + ".jpg")
    print(metadata)

# Close the camera at the end
picam2.close()
