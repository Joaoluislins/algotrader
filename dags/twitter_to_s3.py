# DAG to ingest user's timeline from twitter to am aws s3 instance.

# Importing modules and libraries
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
import requests
import os
import json
import pandas as pd
import time
import backoff
import ratelimit
import logging
from traitlets.traitlets import Union
from aws.bucket import Bucket
import twitter
from twitter.timeline_ingestor import TimelineIngestor




# Configuring Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

# Defining the usernames that will be crawled and instanting classes
usernames = ['cafecomferri', 'FariaLimaElevat', 'helocruz']
ingestor = TimelineIngestor(writer = twitter.data_writer.DataWriter, usernames = usernames)
bucket_client = Bucket('algotrader-joao')

# Default arguments for the DAG
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0)
}

# Creating the DAG and it's tasks
dag = DAG(
    dag_id='twitter_to_s3',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=1)
)

t1 = PythonOperator(
    task_id='ingest_twitter_to_ec2',
    python_callable=ingestor.ingest,
    dag=dag
)

t2 = PythonOperator(
    task_id='start_bucket',
    python_callable=bucket_client.start_bucket,
    dag=dag
)

t3 = PythonOperator(
    task_id='send_twitter_data_to_bucket',
    python_callable=bucket_client.send_to_bucket,
    dag=dag
)

# Task's order
t1 >> t2 >> t3
