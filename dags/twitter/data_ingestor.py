#Creating a general class to ingest data
from abc import ABC,abstractmethod
from twitter.data_writer import DataWriter

class DataIngestor(ABC):

  def __init__(self, writer: DataWriter, usernames: list) -> None:
    self.writer = writer
    self.usernames = usernames
    self._checkpoint = self.load_checkpoint()
    
    

  @property
  def _checkpoint_filename(self):
    return f"{self.__class__.__name__}.checkpoint"

  def _write_checkpoint(self,user_id):
    path = f"/opt/airflow/outputs/timelines/{user_id}/" # /content is pretty much the root. you can choose other path in your colab workspace
    os.chdir(path)
    with open(self._checkpoint_filename, 'w') as f:
      f.write(f"{self._checkpoint}")  

  def load_checkpoint(self) -> str:
    try:
      path = f"/opt/airflow/outputs/timelines/{self.user_id}/" # /content is pretty much the root. you can choose other path in your colab workspace
      os.chdir(path)
      with open(self._checkpoint_filename, 'r') as f:
        return f.read()
    except FileNotFoundError:
      return None
    except AttributeError:
      return None
    


  def _get_checkpoint(self) -> str:
    if not self._checkpoint:
      return None
    else:
      return self._checkpoint

  def _update_checkpoint(self, value, user_id):
        self._checkpoint = value
        self.user_id = user_id
        self._write_checkpoint(user_id = user_id)

  @abstractmethod
  def ingest(self) -> None:
    pass