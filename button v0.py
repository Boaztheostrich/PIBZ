from picamera2 import Picamera2, Preview
import time
from datetime import datetime
from gpiozero import Button
from signal import pause
picam2 = Picamera2()
button = Button(16)
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
def capture():
    picam2.start_preview(Preview.QTGL)
    timestamp = datetime.now().isoformat()
    picam2.start()
    time.sleep(2)
    picam2.capture_file('/home/boaz/Desktop/images/%s.jpg' % timestamp)
    picam2.stop_preview()
    picam2.stop()
button.when_pressed = capture
pause()
