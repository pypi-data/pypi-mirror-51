from .base_files_connector import BaseFileConnector
from cnvrg.modules.dataset import Dataset
from cnvrg.helpers.apis_helper import url_join

class DatasetConnector(BaseFileConnector):

    @staticmethod
    def key_type():
        return "dataset"

    def __init__(self, dataset=None, working_dir=None):
        super(DatasetConnector, self).__init__(dataset)
        self.__files = None
        self.__dataset = Dataset(url_join(self._org, self._data_connector), working_dir=working_dir)

    @property
    def working_dir(self):
        return self.__dataset.get_working_dir()

    def __len__(self):
        if not self.__files: self.__files = self._files_callback(self.__dataset.fetch_all_files())
        return len(self.__files)

    def __getitem__(self, item):
        return self.__dataset.download_file(self.__files[item])