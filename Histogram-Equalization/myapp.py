# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tk
import threading
import datetime
import imutils
import cv2
import os


class MyApp:
    def __init__(self, vs, oPath):
        ''' store the video stream object and output path, then initialize
         the most recently read frame, thread for reading frames, and
         the thread stop event'''
        self.vs = vs
        self.oPath = oPath
        self.frame = None
        self.thread = None
        self.stopEvent = None

        # initialize the root window and panel
        self.root = tk.Tk()
        self.panel = None

        topFrame = tk.Frame(self.root)
        topFrame.pack(side='top')
        bottomFrame = tk.Frame(self.root)
        bottomFrame.pack(side='bottom')
       
       

        ''' create a button, that when pressed, will take the current
         frame and save it to file'''
        btn = tk.Button(bottomFrame, text="ClickPic!",
                         command=self.takesnapshot)
        btn1 = tk.Button(bottomFrame, text="video!",
                        command=self.videoLoop)
        browsebutton = tk.Button(topFrame, text="Browse",  
        command=self.browsefunc)
        pathlabel = tk.Label(self.root)
        pathlabel.pack()
        btn.pack(side="left", fill="both", expand="yes", padx=10,
                 pady=10)
        btn1.pack(side="right", fill="both", expand="yes", padx=10,
                 pady=10)
        browsebutton.pack(side="left", fill="both", expand="yes", padx=10,
                 pady=10)

        ''' start a thread that constantly pools the video sensor for
         the most recently read frame'''
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("PyImageSearch")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def videoLoop(self):
        
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                '''grab the frame from the video stream and resize it to
                   have a maximum width of 300 pixels'''
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)

                # OpenCV represents images in BGR order
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tk.Label(image=image)
                    self.panel.image = image
                    self.panel.pack(side="left", padx=10, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError as e:
            print("RuntimeError")

    def takesnapshot(self):
        ''' grab the current timestamp and use it to construct the
         output path'''
        ts = datetime.datetime.now()
        filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
        p = os.path.sep.join((self.oPath, filename))

        # save the file
        cv2.imwrite(p, self.frame.copy())
        print("[INFO] saved {}".format(filename))

    def onClose(self):
        ''' set the stop event, cleanup the camera, and allow the rest of
         the quit process to continue'''
        print("closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
   def browsefunc(self):
        # for brosewing the image/video file from local computer
        filename = filedialog.askopenfilename()
        pathlabel.config(text=filename)
