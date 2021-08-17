import os
import subprocess
import sys
from secrets import token_hex

import matplotlib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from .exceptions import FunctionNotFoundError
matplotlib.use('Agg')


class StatistantCalc:
    def __init__(self, df, filename: str = None, func: str = None):
        self.df = df
        self.filename = filename
        self.func = func
        self.selected = None

        directory = f"statistant/results/{self.func}_{self.filename}_{token_hex(5)}.png"
        parent_dir = os.path.expanduser("~")
        self.path = os.path.join(parent_dir, directory)

    @staticmethod
    def open_file(filepath):
        """
        function for open files in Directory

        Parameters
        -------
        filepath
            path of file which should be opened
        """
        if sys.platform == "win32":
            os.startfile(filepath)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filepath])

    def stats_basic(self, func: str, col: str, interval=False, lower: int = None, upper: int = None):
        """
        Function for statistical basic functions.

        Parameters
        ----------
        func
            is the function name which should be called.
            Possible function names are: average, median, mode, variance, standard deviation, min, max, sum
        col
            is the column which should be selected
        interval
            [optional] bool if there should be an interval as selected or not
        lower
            [optional] lower value of selected interval
        upper
            [optional] upper value of selected interval

        Returns
        -------
        result
            result (=value) of called function

        """
        # .astype() for fallback for int64
        self.do_selection(interval, col, lower, upper)
        # function chooser
        df = self.selected
        function = {
            "average": df.mean,
            "median": df.median,
            "variance": df.var,
            "mode": df.mode().to_list,
            "standard deviation": df.std,
            "smallest value": df.min,
            "top value": df.max,
            "sum": df.sum,
            "quartile range": self.iqr,
            "range": self.data_range
        }
        # safe call for function chooser
        if func in function.keys():
            result = function[func]()
        else:
            raise FunctionNotFoundError(f"Function {func} is not a valid function")

        # mode is a list because in some cases there can be more modes than one
        # -> mode can not be rounded because of list type
        return result if type(result) == list or result is None else round(result, 3)

    def mean_2_cells(self, val1, val2, col):
        mean = round(self.df.loc[self.df.index[[val1 - 1, val2 - 1]], col].mean(), 3)
        return mean

    def iqr(self):
        q1 = self.selected.quantile(0.25)
        q3 = self.selected.quantile(0.75)
        iqr = q3 - q1
        return iqr

    def data_range(self):
        data_range = self.selected.max() - self.selected.min()
        return data_range

    def quantiles(self, col, percentile, interval=False, lower: int = None, upper: int = None):
        self.do_selection(interval, col, lower, upper)
        quantile = self.selected.quantile(percentile)
        return round(quantile, 3)

    def do_selection(self, interval, col, lower, upper):
        if not interval:
            self.selected = self.df[col].astype('float64')
        else:
            if lower > upper:
                lower, upper = upper, lower
            # select interval
            self.selected = self.df.loc[self.df.index[(lower - 1):upper], col].astype('float64')

    def cluster(self, x_col: str, y_col: str, num_clusters: int,
                title: str = None, x_label: str = None, y_label: str = None):
        """
        function for calculating, visualize and save the cluster analysis

        Parameters
        -------
        x_col
            is the column which should be selected for the x-axis
        y_col
            is the column which should be selected for the y-axis
        num_clusters
            number of cluster which should be used for cluster analysis
        title
            [optional] title for plot
        x_label
            [optional] label for x-axis of plot
        y_label
            [optional] label for y-axis of plot
        """

        df = self.df
        x_col = self.df[x_col]
        y_col = self.df[y_col]

        # variables for cluster analysis
        kmeans = KMeans(n_clusters=num_clusters).fit(df)
        centroids = kmeans.cluster_centers_

        # init plot
        plt.scatter(x_col, y_col, c=kmeans.labels_.astype(float), s=70, alpha=0.5)
        plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)

        # optional adjustments by user
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # save plot in Directory
        plt.savefig(self.path)
        plt.clf()

        # Open plot
        self.open_file(self.path)
