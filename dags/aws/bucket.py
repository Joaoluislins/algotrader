# Creating an aws client to manage bucket resources
from dotenv import load_dotenv
from os import getenv
from abc import ABC, abstractmethod
import boto3
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

load_dotenv('/opt/airflow/outputs/.env')

class Bucket(ABC):
    def __init__(self) -> None:
        
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


    def start_bucket(self, bucket_name) -> None:
        self.bucket_name = bucket_name
        if not self._validate_bucket():
            self._criar_bucket()     
        else:
            print(f'Bucket "{self.bucket_name}" already existed (and operational?)')


    def send_to_bucket(self) -> None:
        sending_datetime = datetime.now().strftime("%Y%m%d_%H%S%S")
        self.s3_resource.Bucket(self.bucket_name).upload_file(
            f'/opt/airflow/outputs/timelines/{ingestor.user_id}/{ingestor.writer.filename}',
            f'airflow/dados/input/twitter_{sending_datetime}_{ingestor.writer.filename}'
        )


