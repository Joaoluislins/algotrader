<<<<<<< HEAD
from twitter.twitter_api import TwitterAPI
import logging
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv('/opt/airflow/aws_twi_env/.env')

# Creating a specific class to interact with get_users_id endpoint.
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class GetUsersInfo(TwitterAPI):

  def __init__(self, names: list, **kwargs) -> None:
    self.names = names
    self.usernames = "usernames={}".format(','.join(self.names))
    self.type_of_endpoint = 'users/by?{}&{}' #Specific to get users_id
    self.user_fields = user_fields = "user.fields=description,created_at,id"
    self.bearer_token = bearer_token = getenv('BEARER_TOKEN') 
    #self.bearer_oauth = bearer_oauth
    super().__init__(**kwargs)

  # Specify the usernames that you want to lookup below
  # You can enter up to 100 comma-separated values.
  
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld

  def _get_endpoint(self) -> str:
    return f"{self.base_endpoint}/{self.type_of_endpoint}".format(self.usernames, self.user_fields)


  def connect_to_endpoint(self, url):
    response = requests.request("GET", url, auth = self.bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

  
  def get_data(self, **kwargs) -> dict:
    #bearer_token =  ## encript this call
    url = self._get_endpoint()
    logger.info(f"getting data from endpoint: {url}")
    response = self.connect_to_endpoint(url)
=======
from twitter.twitter_api import TwitterAPI
import logging
import requests
from dotenv import load_dotenv
from os import getenv

load_dotenv('/opt/airflow/aws_twi_env/.env')

# Creating a specific class to interact with get_users_id endpoint.
logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class GetUsersInfo(TwitterAPI):

  def __init__(self, names: list, **kwargs) -> None:
    self.names = names
    self.usernames = "usernames={}".format(','.join(self.names))
    self.type_of_endpoint = 'users/by?{}&{}' #Specific to get users_id
    self.user_fields = user_fields = "user.fields=description,created_at,id"
    self.bearer_token = bearer_token = getenv('BEARER_TOKEN') 
    #self.bearer_oauth = bearer_oauth
    super().__init__(**kwargs)

  # Specify the usernames that you want to lookup below
  # You can enter up to 100 comma-separated values.
  
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld

  def _get_endpoint(self) -> str:
    return f"{self.base_endpoint}/{self.type_of_endpoint}".format(self.usernames, self.user_fields)


  def connect_to_endpoint(self, url):
    response = requests.request("GET", url, auth = self.bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

  
  def get_data(self, **kwargs) -> dict:
    #bearer_token =  ## encript this call
    url = self._get_endpoint()
    logger.info(f"getting data from endpoint: {url}")
    response = self.connect_to_endpoint(url)
>>>>>>> 7e07a03657318a5b7652ebb8634b07f3a163c215
    return response