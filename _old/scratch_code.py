import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()

# this is how you change the image resolution
# config = picam.create_preview_configuration(main={"size":(1600, 1200)})
preview_config = picam.create_preview_configuration(main={"size": (4056, 3040)}, lores={"size": (640, 480)}, display="lores")
# capture_config = picam.create_still_configuration
# config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam.configure(preview_config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(10)
picam.capture_file("test-python.jpg")

picam.close()


# look at buffer count to make it smoother maybe