#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox
from picamera2 import Picamera2, Preview
import time
import sys

picam2 = Picamera2()
# this is how you change the image resolution
config = picam2.create_preview_configuration(main={"size":(1600, 1200)})
picam2.configure(config)
picam2.start_preview(Preview.QTGL)
picam2.start()

root = Tk()
root.title(sys.argv[0])
root.geometry("200x200")
# center on screen
root.eval('tk::PlaceWindow . center')

labelframe = LabelFrame(root, text="Click button to capture image")
labelframe.pack(fill = "both", expand = "yes")

def btnCallBack():
    print("- Capture image -")
    timeStamp = time.strftime("%Y%m%d-%H%M%S")
    targetPath="/home/boaz/Desktop/images/img_"+timeStamp+".jpg"
    picam2.capture_file(targetPath)
    print("image save:", targetPath)
    print("----------------------------------------------------")

B = Button(labelframe, text ="Capture", command = btnCallBack, width=100, height=100)

B.pack()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        picam2.stop_preview()
        root.destroy()
        
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
