import cv2
import os 
import argparse
import time


class VIDEOTOIMAGE:
    def __init__(self,videopath, framerate):
        self.vs = cv2.VideoCapture(videopath)
        self.framerate = framerate
        
        # Output folder for the images
        self.OUTPUTPATH = os.path.join(os.path.dirname(__file__), "images")
        if not os.path.exists(self.OUTPUTPATH):
            os.makedirs(self.OUTPUTPATH)
            
    def __getFrame(self, sec):
        # Function to capture at fixed timestep based on frame rate
        self.vs.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
        return self.vs.read()
    
    def __saveframe(self, frame):
        # Save the frame
        cv2.imwrite(os.path.join(self.OUTPUTPATH, "image{}.jpg".format(self.__timestamp())), frame)

    def __timestamp(self, ):
        seconds = 0
        minutes = 0
        hours = 0

        milliseconds = self.vs.get(cv2.CAP_PROP_POS_MSEC)
        seconds = milliseconds//1000
        milliseconds = milliseconds%1000
        if seconds >= 60:
            minutes = seconds//60
            seconds = seconds % 60
        if minutes >= 60:
            hours = minutes//60
            minutes = minutes % 60

        return "{}_{}_{}_{}".format(int(hours), int(minutes), int(seconds), int(milliseconds))

    
    def getImages(self, ):
        time.sleep(0.01)
        sec = 0
        while self.vs.isOpened():
            ret, frame = self.__getFrame(sec)
            if ret:
                self.__saveframe(frame)
                sec += self.framerate
                sec = round(sec, 2)
            else:
                break
        time.sleep(0.01)
        v2i.vs.release()
    
def cli():
    # Argument parser
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", required=True,
                    help="Full path to the video for images to be fetched.")
    ap.add_argument("-f", "--framerate", type=float, default=0.5,
                    help="Time between each frames from the video.\nDefault: 0.5 second difference between frames.")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":

    ## SETUP ##
    args = cli()
    v2i = VIDEOTOIMAGE(args["video"], args["framerate"])
    print("[V2I] Generating images at folder {}...".format(v2i.OUTPUTPATH), end= " ")
    v2i.getImages()
    print("Done!")