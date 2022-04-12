# Creating a class to write the ingested data in files.
import os
import json

class DataWriter:

  def __init__(self, api_type: str, user_id: str) -> None:
    self.api_type = api_type
    self.user_id = user_id
    
    self.filename = f"{self.api_type}-{self.user_id}.json"

  def _write_row(self, data: dict) -> None:
    #os.makedirs(os.path.dirname(self.filename), exist_ok = True)
    #print(os.getcwd())
    #os.chdir('/opt/***')
    print(os.getcwd())
    os.chdir('outputs/')
    print(os.getcwd())
    if not os.path.isdir(f"timelines/{self.user_id}/"):
      os.makedirs(os.path.dirname(f"timelines/{self.user_id}/"), exist_ok = True)
    #path = f"timelines/{self.user_id}/"
    os.chdir(path)
    print(os.getcwd())
    with open(f"timelines/{self.user_id}/{self.filename}", 'a') as f:
      for item in data['data']:
        #print(type(item))
        #print(item)
        #f.write(json.dumps(item, indent=4, sort_keys=True))
        json.dump(item, f)
        f.write('\n')
      #files.download(f)


  def write(self, data: str) -> None:
    self._write_row(data)