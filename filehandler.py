import os
import pandas as pd


class FileHandler:
    def __init__(self, filename):
        self.filename = filename

        # init file path
        directory = "statistant"
        parent_dir = os.path.expanduser("~")
        path = os.path.join(parent_dir, directory)
        self.file_path = f"{path}/{filename}"

    def get_file_path(self):
        return self.file_path

    def read_csv(self):
        path = self.file_path
        df = pd.read_csv(path)
        return df
