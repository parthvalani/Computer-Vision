# import the necessary packages
from __future__ import print_function
from myapp import MyApp
from imutils.video import VideoStream
import argparse
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
                help="path to output directory to store ClickPic!s")
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or python camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

# start the app
pba = MyApp(vs, args["output"])
pba.root.mainloop()
