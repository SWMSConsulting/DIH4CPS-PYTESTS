import os
import sys

class CronHandler:

    cronList = []
    outputFile_name = "crontabs.txt"

    cron_every_10min = "*/10 * * * *"
    cron_everyDay_00_05 = "5 0 * * *"

    def __init__(self):
        self.python_path = sys.executable
        self.parentDir_path = os.path.dirname(os.path.realpath(__file__))
        self.outputFile_path = os.path.join(self.parentDir_path, self.outputFile_name)

        self.webcamRecorder_path = os.path.join(self.parentDir_path, "webcam_recorder.py")
        self.cloudConnection_path = os.path.join(self.parentDir_path, "cloud_connection.py")

        self.webcamRecorder_command = "{0} {1}".format(self.python_path, self.webcamRecorder_path)
        self.cloudConnection_command = "{0} {1}".format(self.python_path, self.cloudConnection_path)

        self.webcamRecorder_output = os.path.join(self.parentDir_path, "webcam_recorder.py")
        self.cloudConnection_output = os.path.join(self.parentDir_path, "cloud_connection.py")

   
        pass

    def addCron(self, cron_str, command_str, outputFile_path=None):
        cron = cron_str + " " + command_str
        if not outputFile_path == None:
            cron += " " + outputFile_path 
        self.cronList.append(cron)

    def updateCron(self, index, cron_str, command_str, outputFile_path=None):
        cron = ""
        if index > len(self.cronList)-1: 
            return False
        cron = cron_str + " " + command_str
        if not outputFile_path == None:
            cron += " " + outputFile_path 
        self.cronList[index] = cron
        return True

    def writeCronToFile(self):
        if os.path.exists(self.outputFile_path):
            os.remove(self.outputFile_path)
        with open(self.outputFile_path, mode='a') as f:
            for cron in self.cronList:
                f.write(cron + "\n")
        return True

def updateCrontab(cronFile_path):
    os.system("crontab {0}".format(cronFile_path))

if __name__ == '__main__':
    handler = CronHandler()

    # run WebCamRecorder every 10 minutes
    handler.addCron(handler.cron_every_10min, 
                    handler.webcamRecorder_command, 
                    handler.webcamRecorder_output)

    # run cloundConnection every day at 00:05 AM
    handler.addCron(handler.cron_everyDay_00_05, 
                    handler.cloudConnection_command, 
                    handler.cloudConnection_output)
    
    handler.writeCronToFile()

    # works on linux only
    updateCrontab(handler.outputFile_path)
