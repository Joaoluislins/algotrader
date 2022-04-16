from twitter.twitter_api import TwitterAPI
import logging
import requests
from dotenv import load_dotenv
from os import getenv

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

load_dotenv('/opt/airflow/aws_twi_env/.env')
# Creating a specific class to interact with get_users_timeline endpoint.

class GetUserTimeline(TwitterAPI):
  def __init__(self, user_id: str, pagination_token, **kwargs) -> None:
    self.type_of_endpoint = "users/{}/tweets"
    self.user_id = user_id
    self.pagination_token = pagination_token
    self.bearer_token = bearer_token = getenv('BEARER_TOKEN')
    super().__init__(**kwargs)


  def _get_endpoint(self) -> str:
    return f"{self.base_endpoint}/{self.type_of_endpoint}".format(self.user_id) ### Pegando user_id de user_info


  #ef bearer_oauth(self,r):
  # """
  # Method required by bearer token authentication.
  # """

  # r.headers["Authorization"] = f"Bearer {self.bearer_token}"
  # r.headers["User-Agent"] = "v2UserTweetsPython"
  # return r  

  def get_params(self):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if self.pagination_token == None:
      return {"tweet.fields": "created_at,possibly_sensitive", 'max_results': 100}
    else:
      return {"tweet.fields": "created_at,possibly_sensitive", 'max_results': 100, 'pagination_token':'{}'.format(self.pagination_token)}

  def connect_to_endpoint(self):
    response = requests.request("GET", self._get_endpoint(), auth=self.bearer_oauth, params=self.get_params())
    print('connect_to_endpoint GetUserTimeline', response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


  def get_data(self, **kwargs):
      url = self._get_endpoint()
      params = self.get_params()
      logger.info(f"getting data from endpoint: {self._get_endpoint()}")
      json_response = self.connect_to_endpoint()
      #json_response.raise_for_status() # método específico para saber se chamada requests funcionou.
      #print(json.dumps(json_response, indent=4, sort_keys=True))
      return json_response