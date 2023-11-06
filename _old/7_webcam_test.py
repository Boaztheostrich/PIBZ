from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator
import boto_upload
import numpy as np

from picamera2 import Picamera2
piCam = Picamera2()
# piCam.preview_configuration.main.size=(1280,720)
piCam.preview_configuration.main.format="RGB888"
# piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

# Load YOLO model
model = YOLO('best_2048.pt')

# Open the video file uncomment for windows
# captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # captureDevice = camera (this is a Windows-only workaround)
# cap = captureDevice

# uncomment for mac
# cap = cv2.VideoCapture(0)


# Set the desired resolution (720x1280)
new_width = 2048
new_height = 1152

# Load the image mask
mask_image = cv2.imread('mask_v2.png', cv2.IMREAD_GRAYSCALE)  # image must be black and white
resized_mask = cv2.resize(mask_image, (new_width, new_height))
binary_mask = resized_mask // 255  # Convert to binary mask (0s and 1s)

# Initialize car count
car_count = 0

while True:
    
    frame = piCam.capture_array()

    if frame is None:
        break

    # Resize the frame to the desired resolution
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Apply the binary mask to the resized frame
    masked_frame = cv2.bitwise_and(resized_frame, resized_frame, mask=binary_mask)

    # Convert to RGB
    img = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2RGB)

    cv2.imshow('mask', masked_frame)

    # Perform object detection
    results = model.predict(masked_frame, conf=0.4, iou=0.7)  # .4 conf and .7 iou work well

    for r in results:
        annotator = Annotator(resized_frame)  # this has to be put here

        boxes = r.boxes
        for box in boxes:
            car_count += 1  # adds 1 to car count per box
            b = box.xyxy[0]
            annotator.box_label(b)

    frame_with_boxes = annotator.result()  # IDK how to fix this error
    cv2.imshow('YOLO V8 Detection', frame_with_boxes)

    # Calculate remaining count
    remaining_count = 75 - car_count

    # Print the remaining count
    print(f'Remaining Count: {remaining_count}')

    boto_upload.data_string = str(remaining_count)  # it has to be converted to a string

    boto_upload.string_to_aws()  # could be good to include some error logic

    # Reset car count
    car_count = 0  # otherwise it goes to negative infinity

    if cv2.waitKey(1) & 0xFF == ord(' '):  # if you press the space-bar key, it stops the program
        break

cap.release()
cv2.destroyAllWindows()
