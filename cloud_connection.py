"""
CloudConnection: This class rules the cloud connection (S3 architecture) using boto.

Requirements:                    
pip install boto3, see https://pypi.org/project/boto3/ for more informations.
also see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html.

@authors:   Arno Schiller (AS)
@email:     schiller@swms.de
@version:   v0.0.3
@license:   ...

VERSION HISTORY
Version:    (Author) Description:                                           Date:
v0.0.1      (AS) First initialize. Tested example code for S3 storage.      05.08.2020\n
v0.0.2      (AS) First version to save data to the cloud into the           05.08.2020\n
                test-dih4cps bucket.                                                  \n
v0.0.2      (AS) Added functionality to upload every file created on the    05.08.2020\n
                selected day. Starting this script will run the function              \n
                for yesterday.                                                        \n
v0.0.3      (AS) Added logging.                                             06.08.2020\n

ToDo:   - Add return value to the functions (bool)
"""
import boto3
from botocore.exceptions 
import os
import glob
import datetime
from datetime import timedelta
import logging

class CloudConnection:
    """ 
    This class 
    
    Attributes:
    -----------
    access_key : str
        access key (username) of the cloud
    secret_key : str
        secret key (password) of the cloud
    bucket_name : str
        used bucket to save the data to
    cloud_url : str
        url to cloud server
    recordsDir_name : str
        directory the video data is placed in
    max_tries : int
        max number of tries to connect to cloud. 
    """
    access_key = "minio"
    secret_key = "miniostorage"
    bucket_name = "test-dih4cps"
    cloud_url = "https://minio.dih4cps.swms-cloud.com:9000/"

    recordsDir_name = "Recordings"
    max_tries = 10

    def __init__(self):
        """
        Setup the S3 connection and the used bucket. Also define the recordings directory.
        """
        logging.basicConfig(level=logging.INFO)
        logging.info("Initialize CloudConnection.")

        # setup the S3 client
        counter_tries = 0
        self.s3_client = None
        while self.s3_client == None:
            if counter_tries == 0:
                logging.info("Connecting to S3 server...")
            if counter_tries > self.max_tries:
                logging.error("Can not connect to S3 server ({0} tries). Quitting...".format(counter_tries))
                exit()
            self.s3_client = boto3.client('s3', 
                aws_access_key_id = self.access_key,
                aws_secret_access_key = self.secret_key,
                endpoint_url=self.cloud_url, 
                config=boto3.session.Config(signature_version='s3v4'))
            counter_tries += 1
        logging.info("Connected to S3 server.")

        # get directory 
        parentDir_path = os.path.dirname(os.path.realpath(__file__))
        self.recordsDir_path = os.path.join(parentDir_path, self.recordsDir_name)

    def setBucketName(self, bucket_name):
        # Retrieve the list of existing buckets
        s3 = boto3.client('s3')
        response = s3.list_buckets()

        for bucket in response['Buckets']:
            if bucket['Name'] == bucket_name:
                self.bucket_name = bucket_name

    def uploadFileToCloud(self, file_name, object_name=None):
        """Upload a file to an S3 bucket

        Parameters
        ----------
        file_name : str 
            file to upload
        object_name : str 
            S3 object name, if not specified then file_name is used

        Returns
        ----------
        true    if upload was successfull
        false   otherwise
        """
        if object_name == None:
            object_name = file_name
        logging.info("Uploading file {0} ...".format(object_name))
        file_path = os.path.join(self.recordsDir_path, file_name)
        try:
            self.s3_client.upload_file(file_path, self.bucket_name,object_name, Callback=ProgressPercentage(file_path))
            logging.info("Uploading file {0} done".format(object_name))
            return True
        except FileNotFoundError:
            logging.error("The file to upload was not found.")
            return False
        except NoCredentialsError:
            logging.error("Credentials are not available.")
            return False
        except ClientError:
            logging.error("Client Error")
            return False


    def uploadFilesFromDay(self, recording_name, day_datetime):
        """ Upload every avi file that was created on that day.

        Parameters
        ----------
        day_datetime : datetime 
            day as datetime object to save the files from
        recording_name : str
            representative name for clear attribution of the recording (see WebcamRecorder)
        """
        logging.info("Upload files from {0} ...".format(day_datetime))
        # create the filter string
        filter_str = "{0}_{1}-{2:02d}-{3:02d}_*-*-*.avi".format(recording_name, 
                                    day_datetime.year,
                                    day_datetime.month,
                                    day_datetime.day)
        filter_path = os.path.join(self.recordsDir_path, filter_str)
        file_paths = glob.glob(filter_path)

        for path in file_paths:
            file_name = os.path.basename(path)
            self.uploadFileToCloud(file_name)
        logging.info("Upload files from {0} done.".format(day_datetime))

import sys
import threading
class ProgressPercentage(object):
    """ This class is used to show the progress percentage while uploading files.
    Source: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html
    """
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        print("\n")

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    os.path.basename(self._filename), self._seen_so_far, 
                    self._size, percentage))
            sys.stdout.flush()
    
         
def sendFilesFromYesterday():
    s3Con = CloudConnection()
    yesterday = datetime.datetime.now() - timedelta(days = 1)
    s3Con.uploadFilesFromDay("test1", yesterday)

if __name__ == "__main__":
    sendFilesFromYesterday()

