#Creating a specific class to ingest data from the user's timeline endpoint
from twitter.data_ingestor import DataIngestor
from twitter.get_users_info import GetUsersInfo
from twitter.get_users_timeline import GetUserTimeline

class TimelineIngestor(DataIngestor):
  
  def ingest(self) -> None:
    
    users_info = GetUsersInfo(self.usernames).get_data()['data']
    print(users_info)
    
    for user in users_info:
      self.user_id = user['id']
      self._checkpoint = self.load_checkpoint()
      print(self.user_id)

      ###Getting the first page

      pagination_token = self._get_checkpoint() ### getting the most recent pagination token from the checkpoint file

      api = GetUserTimeline(pagination_token = pagination_token, user_id = self.user_id)
      data = api.get_data()
      self.writer(api_type = 'timeline', user_id = self.user_id).write(data) #Writing the data in the file 
      self._update_checkpoint(data['meta']['next_token'], self.user_id) # updating the checkpoint file
      print('Saved data from pagination token:', data['meta']['next_token']) 


      while (data['meta']['next_token']): #Getting the remaining pages

        pagination_token = self._get_checkpoint() ### getting the most recent pagination token from the checkpoint file
        api = GetUserTimeline(pagination_token = pagination_token, user_id = self.user_id)
        data = api.get_data()
        self.writer(api_type = 'timeline', user_id = self.user_id).write(data) #Writing the data in the file 
        try:
          self._update_checkpoint(data['meta']['next_token'], user_id = self.user_id) # updating the checkpoint file
          print('Saved data from pagination token:', data['meta']['next_token'])
        except KeyError:
          break