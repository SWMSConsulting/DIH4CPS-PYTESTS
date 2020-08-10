"""
WebcamRecorder: This class rules the recording of video data and saves the data into an avi file. 

Requirements:
- opencv: pip install opencv-python 
    see - https://www.learnopencv.com/install-opencv-4-on-raspberry-pi/
        - https://medium.com/@aadeshshah/pre-installed-and-pre-configured-raspbian-with-opencv-4-1-0-for-raspberry-pi-3-model-b-b-9c307b9a993a

@authors:   Arno Schiller (AS)
@email:     schiller@swms.de
@version:   v0.0.5
@license:   ...

VERSION HISTORY
Version:    (Author) Description:                                           Date:
v0.0.1      (AS) First initialize. Added code from example files and        04.08.2020\n
                solved some problems. Reading and writing video data                  \n
                works fine on PC and Nvidia Jetson Nano                               \n
v0.0.2      (AS) Added generic name to recording files.                     04.08.2020\n
v0.0.3      (AS) First version using CronTab.                               05.08.2020\n
v0.0.4      (AS) Outsourced crontab to system (see README.txt)              05.08.2020\n
v0.0.5      (AS) Added logging.                                             06.08.2020\n
"""

import cv2
import os, datetime
import logging, time

class WebcamRecorder:
    """ 
    This class rules the recording of video data and saves the data into an avi file.
    The file name will be generated like "IDENTIFIER_YEAR_MONTH_DAY_HOUR_MINUTE".
    
    Attributes:
    -----------
    recording_name : str
        representative name for clear attribution of the recording
    fps : int
        frames per second. 
    videolength_s : int
        length of the video to record in seconds. 
    videolength_frames : int
        number of frames used to record video with given length.
    max_tries : int
        max number of tries to open camera/VideoWriter. 
    connection_str : str 
        camera url to connect to like: "rtsp://USERNAME:PASSWORD@IP:PORT"
    """
    recording_name = "test1"
    fps = 20
    videolength_s = 10
    videolength_frames = fps * videolength_s
    max_tries = 5
    connection_str = "rtsp://admin:admin@192.168.8.22:8554"

    def __init__(self):
        """ Setup video capture and video writer. 
        """
        logging.basicConfig(level=logging.INFO)
        logging.info("Initialize WebcamRecorder.")

        # create folder if it does not exist
        parentDir_path = os.path.dirname(os.path.realpath(__file__))
        recordsDir_name = "Recordings"
        recordsDir_path = os.path.join(parentDir_path, recordsDir_name)
        if not os.path.exists(recordsDir_path):
            os.mkdir(recordsDir_path)

        # generate file name
        currentDateTime = datetime.datetime.now()
        file_name = "{0}_{1}-{2:02d}-{3:02d}_{4:02d}-{5:02d}-{6:02d}.avi".format(self.recording_name, 
                                        currentDateTime.year, 
                                        currentDateTime.month,
                                        currentDateTime.day,
                                        currentDateTime.hour,
                                        currentDateTime.minute,
                                        currentDateTime.second)
        file_path = os.path.join(recordsDir_path, file_name)

        # initialize video capture
        self.capture = cv2.VideoCapture(self.connection_str)

        counter_tries = 1
        while not self.capture.isOpened():
            if counter_tries > self.max_tries:
                logging.error("Can not connect to camera ({0} tries). Quitting...".format(counter_tries))
                exit()

            logging.warning("Can not connect to camera. Retrying...")
            time.sleep(2)
            self.capture = cv2.VideoCapture(self.connection_str)
            counter_tries += 1
        logging.info("Connected to camera.")
        # initialize video writer
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))
    
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        self.writer = cv2.VideoWriter(file_path, fourcc, self.fps, (self.frame_width, self.frame_height))
        
        counter_tries = 1
        while not self.writer.isOpened():
            if counter_tries > self.max_tries:
                logging.error("Can not open file writer ({0} tries). Quitting...".format(counter_tries))
                exit()

            logging.warning("Can not open file writer. Retrying...")
            time.sleep(5)
            self.writer = cv2.VideoWriter(file_path, fourcc, self.fps, (self.frame_width, self.frame_height))
            counter_tries += 1
        logging.info("VideoWriter is open.")


    def setVideoLength(self, newLength_s):
        """
        Set new video length in seconds and calculate used number of frames. 
        
        Parameters
        ----------
        newLength_s : int
            new videolength in seconds
        """
        self.videolength_s = newLength_s
        self.videolength_frames = self.fps * self.videolength_s

    def record(self):
        """
        Records video and saves it to output file. 
        """
        logging.info("Started recording.")
        counter_frames = 0
        while(self.capture.isOpened()):
            ret, frame = self.capture.read()
            if ret == True:
               
                # write frame to output file
                self.writer.write(frame)

                # display frame 
                # cv2.imshow('frame',frame)
                
                counter_frames += 1

                # keyboard interrupt 
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logging.info("Keyboard interrupt.")
                    break

                # recording completed
                if counter_frames >= self.videolength_frames:
                    logging.info("Recording completed.")
                    break

            else:
                if not self.capture.isOpened():
                    logging.error("Lost connection to camera.")
                logging.error("Can not read from VideoCapture.")
                break

    def release(self):
        """
        Release everything and close open windows.
        """            
        self.capture.release()
        self.writer.release()
        cv2.destroyAllWindows()

def doRecord():
    recorder = WebcamRecorder()
    recorder.record()
    recorder.release()

if __name__ == "__main__":
    doRecord()
