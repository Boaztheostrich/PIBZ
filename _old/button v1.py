from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from gpiozero import Button
from signal import pause
picam2 = Picamera2()
button = Button(16)
camera_config = picam2.create_preview_configuration(main={"size": (4056, 3040)}, lores={"size": (480, 360)}, display="lores", buffer_count=5)
picam2.configure(camera_config)

def capture():
    # picam2.start_preview(Preview.QTGL)
    # timestamp = datetime.now().isoformat()
    # picam2.start()
    # time.sleep(2)
    # metadata= picam2.capture_file('/home/boaz/Desktop/images/%s.jpg')
    # metadata= picam2.capture_file('/home/boaz/Desktop/images/%s.jpg' % timestamp)

    # picam2.stop_preview()
    # picam2.stop()
    metadata = picam2.capture_file("/home/boaz/Desktop/images/" + time.strftime("%Y%m%d-%H%M%S") + ".jpg")
    print(metadata)

picam2.start_preview(Preview.QTGL, width=549, height=412)
picam2.start()

while True:
    button.when_pressed = capture
# pause()
