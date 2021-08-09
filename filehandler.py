import os
import pandas as pd
from .exceptions import FileNotUniqueError


class FileHandler:
    """
    This class represents all operations for handling a file.

    Attributes
    ----------
    filename : str
        name of the file. contains the name+file type. e.g. 'test.csv'
    file_path : str
        path of the file as String
    dir_path : str
        path of the 'statistant' directory
    type : str
        file type of the file
    content : DataFrame
        content of the file as a DataFrame. Can be used for calculations
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

        # init directory path
        directory = "statistant"
        parent_dir = os.path.expanduser("~")
        path = os.path.join(parent_dir, directory)
        self.dir_path = path

        # search for correct file because filename has no type
        files = os.scandir(self.dir_path)
        search_result = [file.name for file in files if
                         file.name.split(".", 1)[0] == filename.lower() and file.is_file()]
        files.close()

        # If no result (=empty), raise FileNotFound Error
        # if search result has more than 1 result, file cannot identified -> FileNotUnique Error
        if not search_result:
            raise FileNotFoundError("File not found")
        elif len(search_result) > 1:
            raise FileNotUniqueError("File has no unique name and hence cannot be identified")

        self.filename = search_result[0]
        self.file_path = f"{self.dir_path}/{self.filename}"

        # init type
        self.type = self.filename.split(".", 1)[1]

        # init content
        # For future adding supported type: add type ending as key and reading function as value. no more actions to do
        type_chooser = {
            'csv': self.read_csv,
            'txt': self.read_csv,  # reading txt-files has to be done with read_csv too
            'xlsx': self.read_xlsx,
            'json': self.read_json,
            'pkl': self.read_pickle,
            'h5': self.read_hdf
        }
        self.content = type_chooser[self.type]()

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
        df.columns = df.columns.str.lower()
        return df

    def read_xlsx(self):
        """
        function for reading the file as xlsx

        Returns
        -------
        df : DataFrame
            DataFrame of reading result
        """
        path = self.file_path
        df = pd.read_excel(path, engine="xlrd")
        df.columns = df.columns.str.lower()
        return df

    def read_json(self):
        """
        function for reading the file as json

        Returns
        -------
        df : DataFrame
            DataFrame of reading result
        """
        path = self.file_path
        df = pd.read_json(path)
        df.columns = df.columns.str.lower()
        return df

    def read_pickle(self):
        """
        function for reading the file as pickle

        Returns
        -------
        df : DataFrame
            DataFrame of reading result
        """
        path = self.file_path
        df = pd.read_pickle(path)
        df.columns = df.columns.str.lower()
        return df

    def read_hdf(self):
        """
        function for reading the file as h5

        Returns
        -------
        df : DataFrame
            DataFrame of reading result
        """
        path = self.file_path
        df = pd.read_hdf(path)
        df.columns = df.columns.str.lower()
        return df
