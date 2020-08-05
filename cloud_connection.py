"""
CloudConnection: This class rules the cloud connection (S3 architecture) using boto.

Requirements:                    
pip install boto3, see https://pypi.org/project/boto3/ for more informations.
also see https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-uploading-files.html.

@authors:   Arno Schiller (AS)
@email:     schiller@swms.de
@version:   v0.0.2
@license:   ...

VERSION HISTORY
Version:    (Author) Description:                                           Date:
v0.0.1      (AS) First initialize. Tested example code for S3 storage.      05.08.2020\n
v0.0.2      (AS) First version to save data to the cloud into the           05.08.2020\n
                test-dih4cps bucket.                                                  \n

ToDo:   - Add return value to the functions (bool)
"""
import boto3
import os

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
    recordsDir_name : str
        directory the video data is placed in
    """
    access_key = "minio"
    secret_key = "miniostorage"
    bucket_name = "test-dih4cps"

    recordsDir_name = "Recordings"

    def __init__(self):
        """
        Setup the S3 connection and the used bucket. Also define the recordings directory.
        """
        self.s3 = boto3.resource('s3', 
            aws_access_key_id = self.access_key,
            aws_secret_access_key = self.secret_key,
            endpoint_url='https://minio.dih4cps.swms-cloud.com:9000/', 
            config=boto3.session.Config(signature_version='s3v4'))

        self.bucket = self.s3.Bucket(self.bucket_name)

        for bucket in self.s3.buckets.all():
            print(bucket.name)

        # get directory 
        parentDir_path = os.path.dirname(os.path.realpath(__file__))
        self.recordsDir_path = os.path.join(parentDir_path, self.recordsDir_name)        

    def uploadFileToCloud(self, file_name, object_name=None):
        """Upload a file to an S3 bucket

        Parameters
        ----------
        file_name : str 
            file to upload
        object_name : str 
            S3 object name, if not specified then file_name is used
        """
        if object_name == None:
            object_name = file_name

        file_path = os.path.join(self.recordsDir_path, file_name)

        data = open(file_path, 'rb')
        self.bucket.put_object(Key=object_name, Body=data)


def sendFiles():
    s3Con = CloudConnection()
    s3Con.uploadFileToCloud("output.avi")

if __name__ == "__main__":
    sendFiles()
