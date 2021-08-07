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

        # init directory path
        directory = "statistant"
        parent_dir = os.path.expanduser("~")
        path = os.path.join(parent_dir, directory)
        self.dir_path = path

        # search for correct fil because filename has no type
        # TODO find faster way
        files = os.listdir(self.dir_path)
        for file in files:
            if file.split(".")[0] == filename:
                filename = file
            else:
                raise FileNotFoundError("Sorry, File cannot found")

        self.file_path = f"{path}/{filename}"
        self.filename = filename

        # init type
        self.type = self.filename.split(".", 1)[1]

        # init content
        # TODO add file types in type_chooser if read functions exists
        type_chooser = {'csv': self.read_csv()}
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
        return df
