import os
import pandas as pd


class FileHandler:
    """
    This class represents all operations for handling a file.

    Attributes
    ----------
    filename : str
        name of the file
    file_path : str
        path of the file as String
    """

    def __init__(self, filename):
        """
        Inits the FileHandler. Set the filename and gives the file
        the right filepath from the directory 'statistant'

        Parameters
        ----------
        filename : str
            is given name of the file
        """
        self.filename = filename

        # init file path
        directory = "statistant"
        parent_dir = os.path.expanduser("~")
        path = os.path.join(parent_dir, directory)
        self.file_path = f"{path}/{filename}"

    def get_file_path(self):
        return self.file_path

    def read_csv(self):
        """
        function for reading the file as csv

        Returns
        -------
        df : DataFrame
            DataFrame of reading result
        """
        path = self.file_path
        df = pd.read_csv(path)
        return df
