from multiprocessing import Process, Value, Lock
from email_sender import sender, email_checker
from sirena import *
import numpy as np		      # importing Numpy for use w/ OpenCV
import cv2                            # importing Python OpenCV
from datetime import datetime         # importing datetime for naming files w/ timestamp

def diffImg(t0, t1, t2):              # Function to calculate difference between images.
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

class Status(object):                # for getting status via emal in multiproc
    def __init__(self, initival=0):
        self.val = Value('i', initival)
        self.lock = Lock()
    
    def set_to_work(self):
        with self.lock:
            self.val.value = 1
    
    def set_out_work(self):
        with self.lock:
            self.val.value = 0
            
    def get_status(self):
        with self.lock:
            return self.val.value

initial()

status = Status(0)

def work_on(status):
    global proc_1, proc_2
    threshold = 160000                     # Threshold for triggering "motion detection"             
    cam = cv2.VideoCapture(0)             # Lets initialize capture on webcam

    winName = "Movement Indicator"	      # comment to hide window
    cv2.namedWindow(winName)              # comment to hide window

    # Read three images first:
    t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    # Lets use a time check so we only take 1 pic per sec
    timeCheck = datetime.now().strftime('%Ss')
    try:
        while True:
            status.set_to_work()
            ret, frame = cam.read()	      # read from camera
            totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus))	# this is total difference number
            text = "threshold: " + str(totalDiff)				# make a text showing total diff.
            cv2.putText(frame, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)   # display it on screen
            is_sirena_stop()
            if totalDiff > threshold and timeCheck != datetime.now().strftime('%Ss'):
                start_sirena()
                dimg= cam.read()[1]
                cv2.imwrite('avast.jpg', dimg)
                sender('avast.jpg')
            timeCheck = datetime.now().strftime('%Ss')
          # Read next image
            t_minus = t
            t = t_plus
            t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
            cv2.imshow(winName, frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print('End')
    finally:    
        cam.release()
        cv2.destroyAllWindows()
        close_sirena()
        print('close')
        proc_1.terminate()
        proc_2.terminate()
        
proc_1 = Process(target=work_on, args=(status,))
proc_2 = Process(target=email_checker, args=(status,))

proc_1.start()
proc_2.start()
