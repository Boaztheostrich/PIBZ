import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()

# this is how you change the image resolution
config = picam.create_preview_configuration(main={"size":(1600, 1200)})
# config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(10)
picam.capture_file("test-python.jpg")

picam.close()