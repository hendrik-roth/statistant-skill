import os
import pandas as pd


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
        files = os.listdir(self.dir_path)
        search_result = [file for file in files if file.split(".")[0] == filename]

        # check if there is a search result for filename. If not (=empty), raise FileNotFound Error else continue
        if not search_result:
            raise FileNotFoundError("File not found")

        self.filename = search_result[0]
        self.file_path = f"{self.dir_path}/{self.filename}"

        # init type
        self.type = self.filename.split(".", 1)[1]

        # init content
        # TODO add file types in type_chooser if read functions exist
        type_chooser = {'csv': self.read_csv(), 'xlsx': self.read_xlsx()}
        self.content = type_chooser[self.type]

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
        df = pd.read_excel(path, engine="openpyxl")
        df.columns = df.columns.str.lower()
        return df
