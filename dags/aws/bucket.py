<<<<<<< HEAD
# Creating an aws client to manage bucket resources
from dotenv import load_dotenv
from os import getenv
import os
from abc import ABC, abstractmethod
from botocore import exceptions
from botocore.exceptions import ClientError
import boto3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

load_dotenv('/opt/airflow/aws_twi_env/.env')

class Bucket(ABC):
    def __init__(self, bucket_name) -> None:

        self.bucket_name = bucket_name
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY')
        )

        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key =getenv('AWS_KEY')
        )

    def _validate_bucket(self) -> bool:
        bucket_list = [bucket.name for bucket in self.s3_resource.buckets.all()]
        if self.bucket_name in bucket_list: #self.s3_client.list_buckets()['Buckets']['Name']:
            print(f'You already have a Bucket with this name: {self.bucket_name}')
            return True
        else:
            print(f'You don\'t have a Bucket created with this name: {self.bucket_name} --> creating..')
            return False 
            
        
    def _create_bucket(self) -> bool:
        try:
            self.s3_client.create_bucket(Bucket = self.bucket_name)
        except ClientError as e:
            print(f'Bucket {self.bucket_name} not created')
            logging.error(e)
            return False
        print(f'Bucket "{self.bucket_name}" successfuly created')
        return True


    def start_bucket(self) -> None:
        if not self._validate_bucket():
            self._create_bucket()     
        else:
            print(f'Bucket "{self.bucket_name}" already existed (and operational?)')


    def send_to_bucket(self, **kwargs) -> None:
        sending_datetime = datetime.now().strftime("%Y%m%d_%H%S%S")
        rootdir = r'/opt/airflow/outputs/timelines'
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                path_str = str(os.path.join(subdir, file))
                file_str = path_str.split(sep = '/')[-1]
                user_id = path_str.split(sep = '/')[-2]
                self.s3_resource.Bucket(self.bucket_name).upload_file(
                    path_str,
                    f'airflow/dados/twitter_timelines/{sending_datetime}/{user_id}/{file_str}'
=======
# Creating an aws client to manage bucket resources
from dotenv import load_dotenv
from os import getenv
import os
from abc import ABC, abstractmethod
from botocore import exceptions
from botocore.exceptions import ClientError
import boto3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

load_dotenv('/opt/airflow/aws_twi_env/.env')

class Bucket(ABC):
    def __init__(self, bucket_name) -> None:

        self.bucket_name = bucket_name
        
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key = getenv('AWS_KEY')
        )

        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id = getenv('AWS_ID'),
            aws_secret_access_key =getenv('AWS_KEY')
        )

    def _validate_bucket(self) -> bool:
        bucket_list = [bucket.name for bucket in self.s3_resource.buckets.all()]
        if self.bucket_name in bucket_list: #self.s3_client.list_buckets()['Buckets']['Name']:
            print(f'You already have a Bucket with this name: {self.bucket_name}')
            return True
        else:
            print(f'You don\'t have a Bucket created with this name: {self.bucket_name} --> creating..')
            return False 
            
        
    def _create_bucket(self) -> bool:
        try:
            self.s3_client.create_bucket(Bucket = self.bucket_name)
        except ClientError as e:
            print(f'Bucket {self.bucket_name} not created')
            logging.error(e)
            return False
        print(f'Bucket "{self.bucket_name}" successfuly created')
        return True


    def start_bucket(self) -> None:
        if not self._validate_bucket():
            self._create_bucket()     
        else:
            print(f'Bucket "{self.bucket_name}" already existed (and operational?)')


    def send_to_bucket(self, **kwargs) -> None:
        sending_datetime = datetime.now().strftime("%Y%m%d_%H%S%S")
        rootdir = r'/opt/airflow/outputs/timelines'
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                path_str = str(os.path.join(subdir, file))
                file_str = path_str.split(sep = '/')[-1]
                user_id = path_str.split(sep = '/')[-2]
                self.s3_resource.Bucket(self.bucket_name).upload_file(
                    path_str,
                    f'airflow/dados/twitter_timelines/{sending_datetime}/{user_id}/{file_str}'
>>>>>>> 7e07a03657318a5b7652ebb8634b07f3a163c215
            )