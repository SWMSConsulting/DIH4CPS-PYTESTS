"""
WebcamRecorder: This class rules the recording of video data and saves the data into an avi file. 

@authors:   Arno Schiller (AS)
@email:     schiller@swms.de
@version:   v0.0.1
@license:   ...

VERSION HISTORY
Version:    (Author) Description:                                           Date:
v0.0.1      (AS) First initialize. Added code from example files and        04.08.2020\n
                solved some problems. Reading and writing video data                  \n
                works fine on PC and Nvidia Jetson Nano                               \n

ToDo:   - Add cronjobs (into a main class)
"""

from cv2 import cv2

class WebcamRecorder:
    """ 
    This class rules the recording of video data and saves the data into an avi file.
    
    Attributes:
    -----------
    fps : int
        frames per second. 
    videolength_s : int
        length of the video to record in seconds. 
    videolength_frames : int
        number of frames used to record video with given length.
    """
    fps = 20
    videolength_s = 5
    videolength_frames = fps * videolength_s

    def __init__(self):
        """
        Setup video capture and video writer. 
        """
        # initialize video capture
        self.capture = cv2.VideoCapture('rtsp://admin:admin@192.168.8.108:8554')

        if not self.capture.isOpened():
            print("Can not open camera")
            exit()

        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # initialize video writer
        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        fps = self.fps
        video_filename = 'output.avi'
        self.writer = cv2.VideoWriter(video_filename, fourcc, fps, (self.frame_width, self.frame_height))

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
        counter_frames = 0
        while(self.capture.isOpened()):
            ret, frame = self.capture.read()
            if ret == True:
               
                # write frame to output file
                self.writer.write(frame)

                # display frame 
                cv2.imshow('frame',frame)
                
                counter_frames += 1

                # keyboard interrupt 
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # recording completed
                if counter_frames >= self.videolength_frames:
                    break

            else:
                break

    def release(self):
        """
        Release everything and close open windows.
        """            
        self.capture.release()
        self.writer.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    recorder = WebcamRecorder()
    recorder.record()
    recorder.release()