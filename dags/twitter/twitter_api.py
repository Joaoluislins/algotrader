from abc import ABC,abstractmethod
import backoff
import ratelimit
import logging
import requests
from traitlets.traitlets import Union

#Creating a general class to interact with Twitter's API (Abstract):

class TwitterAPI(ABC):
  def __init__(self, **kwargs) -> None:
    self.base_endpoint = 'https://api.twitter.com/2'

  @abstractmethod #Condiciona o dev a implementar esse método quando for criar uma classe que herde essa atual.
  def _get_endpoint(self, **kwargs) -> str: #_ no começo do método significa que é um método de uso interno, não vai estar disponível para o usuário.
    pass

  def bearer_oauth(self,r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {self.bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r

  #decoradores utilizados para colocar limites de requests/tempo em get_data, e lidar com alguns possíveis erros de http
  @abstractmethod
  @backoff.on_exception(backoff.expo, ratelimit.exception.RateLimitException, max_tries= 10)
  @ratelimit.limits(calls = 29, period = 30)     
  @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=10)  
  def get_data(self, **kwargs) -> dict:
    pass
