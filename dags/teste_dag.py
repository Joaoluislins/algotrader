# DAG to teste webdriver

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
from technical_data.teste import WebdriverIngestor


# Configuring Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

# Defining the sites that will be crawled and instanting classes

driver = WebdriverIngestor()
#bucket_client = Bucket('algotrader-joao')

# Default arguments for the DAG
args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(0)
}

# Creating the DAG and it's tasks
dag = DAG(
    dag_id='test_ingest_from_google',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=1)
)

t1 = PythonOperator(
    task_id='test_ingest_from_google',
    python_callable=driver.ingest,
    dag=dag
)


# Task's order
t1
