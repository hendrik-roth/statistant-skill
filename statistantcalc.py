import os

from sklearn.cluster import KMeans
from secrets import token_hex
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


class StatistantCalc:
    def __init__(self, df, filename: str = None, func: str = None):
        self.df = df
        self.filename = filename
        self.func = func

        directory = f"statistant/results/{self.func}_{self.filename}_{token_hex(5)}.png"
        parent_dir = os.path.expanduser("~")
        self.path = os.path.join(parent_dir, directory)

    def stats_basic(self, func: str, col: str, interval=False, lower: int = None, upper: int = None):
        """
        Function for statistical basic functions.

        Parameters
        ----------
        func
            is the function name which should be called.
            Possible function names are: average, median, mode, variance, standard deviation, min, max
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
        if not interval:
            df = self.df[col]
        else:
            if lower > upper:
                lower, upper = upper, lower
            # select interval
            df = self.df.loc[self.df.index[(lower - 1):upper], col]
        # function chooser
        function = {
            "average": df.mean,
            "median": df.median,
            "variance": df.var,
            "mode": df.mode,
            "standard deviation": df.std,
            "min": df.min,
            "max": df.max,
        }

        result = round(function[func](), 3)
        return result

    def mean_2_cells(self, val1, val2, col):
        mean = round(self.df.loc[self.df.index[[val1 - 1, val2 - 1]], col].mean(), 3)
        return mean

    def cluster(self, x_col: str, y_col: str, num_clusters, adjustment: str = None, value=None, value_2: int = None):

        df = self.df
        x_col = self.df[x_col]
        y_col = self.df[y_col]

        kmeans = KMeans(n_clusters=num_clusters).fit(df)
        centroids = kmeans.cluster_centers_

        if adjustment == "the title":
            plt.title(value)
        elif adjustment == "the axis labels":
            plt.xlabel(value)
            plt.ylabel(value_2)
        elif adjustment == "the number of clusters":
            kmeans = KMeans(n_clusters=value).fit(df)
        else:
            pass

        plt.scatter(x_col, y_col, c=kmeans.labels_.astype(float), s=70, alpha=0.5)
        plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)

        plt.savefig(self.path)
        plt.clf()
