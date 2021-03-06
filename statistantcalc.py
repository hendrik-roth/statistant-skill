import os
import subprocess
import sys
from secrets import token_hex

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
import statsmodels.formula.api as sm
from sklearn.cluster import KMeans

from .exceptions import FunctionNotFoundError, ChartNotFoundError, HypothesisError

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

    @staticmethod
    def calc_gini(col):
        """

        Parameters
        ----------
        col
            column which should be used for calculating the gini coefficient

        Returns
        -------
        gini
            value of gini coefficient
        """
        col = col.to_numpy()
        diffsum = 0
        for i, xi in enumerate(col[:-1], 1):
            diffsum += np.sum(np.abs(xi - col[i:]))
        gini = (diffsum / (len(col) ** 2 * np.mean(col))).round(3)
        return gini

    @staticmethod
    def calc_herfindahl(col):
        """

        Parameters
        ----------
        col
            column which should be used for calculating the herfindahl index

        Returns
        -------
        herfindahl
            value of herfindahl index
        """
        sum_col = col.sum()
        herfindahl = 0
        for i in col:
            fi_squared = (i / sum_col) ** 2
            herfindahl += fi_squared
        return herfindahl

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
        self.do_selection(col, interval, lower, upper)
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
        elif func == "gini coefficient":
            result = self.calc_gini(df)
        elif func == "herfindahl index":
            result = self.calc_herfindahl(df)
        else:
            raise FunctionNotFoundError(f"Function {func} is not a valid function")

        # mode is a list because in some cases there can be more modes than one
        # -> mode can not be rounded because of list type
        return result if type(result) == list or result is None else round(result, 3)

    def mean_2_cells(self, val1: int, val2: int, col: str):
        """
        function for calculating the mean of 2 cells in one column

        Parameters
        ----------
        val1
            cell 1
        val2
            cell 2
        col
            column of the cells

        Returns
        -------

        """
        mean = round(self.df.loc[self.df.index[[val1 - 1, val2 - 1]], col].mean(), 3)
        return mean

    def iqr(self):
        """
        function for calculating the inter quartile range

        Returns
        -------
        iqr
            inter quartile range
        """
        q1 = self.selected.quantile(0.25)
        q3 = self.selected.quantile(0.75)
        iqr = q3 - q1
        return iqr

    def data_range(self):
        """
        function for calculating the range

        Returns
        -------
        data_range
            range

        """
        data_range = self.selected.max() - self.selected.min()
        return data_range

    def quantiles(self, col: str, percentile: float, interval=False, lower: int = None, upper: int = None):
        """
        function for calculating quantiles

        Parameters
        ----------
        col
            column on which calculation should be performed
        percentile
            percentile of quantile
        interval
            [optional] boolean if interval should be calculated
        lower
            [optional] lower value of interval
        upper
            [optional] upper value of interval

        Returns
        -------
        quantile
            rounded quantile (3 decimals)
        """
        self.do_selection(col, interval, lower, upper)
        quantile = self.selected.quantile(percentile)
        return round(quantile, 3)

    def do_selection(self, col: str, interval=False, lower=None, upper=None):
        """
        functions for performing a selection of a DataFrame. Sets self.selected

        Parameters
        ----------
        col
            column which should be selected (astype float64 for better avoiding json errors)
        interval
            [optional] boolean if interval should be calculated
        lower
            [optional] lower value of interval
        upper
            [optional] upper value of interval
        """
        if not interval:
            self.selected = self.df[col].astype('float64')
        else:
            if lower > upper:
                lower, upper = upper, lower
            # select interval
            self.selected = self.df.loc[self.df.index[(lower - 1):upper], col].astype('float64')
        # drop all NaN in selected interval
        self.selected.dropna(how="all", inplace=True)

    def cluster(self, x_colname: str, y_colname: str, num_clusters: int,
                title: str = None, x_label: str = None, y_label: str = None):
        """
        function for calculating, visualize and save the cluster analysis

        Parameters
        -------
        x_colname
            is the column which should be selected for the x-axis
        y_colname
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
        x_col = self.df[x_colname]
        y_col = self.df[y_colname]

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

    def frequency(self, val: int, col: str, kind: str = "absolute"):
        """
        function for calculating frequency of cell
        Parameters
        ----------
        val
            is the value which should the frequency be calculated
        col
            is column of value
        kind
            kind of frequency: absolute or relative

        Returns
        -------

        """
        return round(self.df[col].value_counts()[val].astype("float64"), 3) if kind == "absolute" else round(
            self.df[col].value_counts()[val].astype("float64") / len(self.df[col]), 3)

    def charts(self, chart: str, x_colname: str = None, y_colname: str = None,
               title: str = None, x_label: str = None, y_label: str = None, x_lim=None, y_lim=None, color=None):
        """
        function for calculating, visualize and save the cluster analysis

        Parameters
        -------
        x_colname
            is the column which should be selected for the x-axis
        y_colname
            is the column which should be selected for the y-axis
        chart
            chart type which should be used for the plot
        title
            [optional] title for plot
        x_label
            [optional] label for x-axis of plot
        y_label
            [optional] label for y-axis of plot
        x_lim
            [optional] limits for x-axis scale
        y_lim
            [optional] limits for y-axis scale
        color
            [optional] color for the plot

        Returns
        -------
        fig
            plot which is created
        """

        df = self.df

        if y_colname is None:
            y_col = y_colname
            x_col = self.df[x_colname]
        elif x_colname is None:
            x_col = x_colname
            y_col = self.df[y_colname]
        else:
            y_col = self.df[y_colname]
            x_col = self.df[x_colname]

        fig, ax = plt.subplots()

        if chart == "histogram":
            ax = sns.histplot(data=df, x=x_col, y=y_col, color=color)
        elif chart in ["bar chart", "barchart", "bar plot", "barplot"]:
            ax = sns.barplot(data=df, x=x_col, y=y_col, color=color)
        elif chart in ["line chart", "linechart", "line plot", "lineplot"]:
            ax = sns.lineplot(data=df, x=x_col, y=y_col, color=color)
        elif chart in ["box plot", "boxplot", "box chart", "boxchart"]:
            ax = sns.boxplot(data=df, x=x_col, y=y_col, color=color)
        elif chart in ["scatter plot", "scatterplot", "scatter chart", "scatterchart"]:
            ax = sns.scatterplot(data=df, x=x_col, y=y_col, color=color)
        else:
            raise ChartNotFoundError(f"{chart} is not a valid charttype")

        ax.set_title(title)

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        if x_lim is not None:
            ax.set_xlim(x_lim[0], x_lim[1])
        if y_lim is not None:
            ax.set_ylim(y_lim[0], y_lim[1])

        return fig

    def pie_charts(self, colname: str, title: str = None):
        """
        function for calculating, visualize and save the cluster analysis

        Parameters
        -------
        colname
            is the column which should be selected for the piechart
        title
            [optional] title for plot


        Returns
        -------
        fig
            pieplot which is created
        """

        df = self.df

        fig, ax = plt.subplots()
        ax.pie(df[colname], labels=df[colname], startangle=90)
        ax.legend(bbox_to_anchor=(1.2, 0.6))
        ax.set_title(title)
        plt.tight_layout()

        return fig

    def simple_regression(self, kind: str, x_col, y_col):
        """
        function for performing a simple regression

        Parameters
        ----------
        kind
            kind of regression (linear or logistic)
        x_col
            column name of x
        y_col
            column name of y
        Returns
        -------
        model
            regression model

        """
        if x_col not in self.df.columns or y_col not in self.df.columns:
            raise KeyError

        formula = f"{y_col}~{x_col}"
        if kind == "logistic":
            # check if values for y are all between 0 and 1
            between = self.df[y_col].between(0, 1).all()
            if not between:
                raise ValueError(f'values of {y_col} are not between 0 and 1')
            model = sm.logit(data=self.df, formula=formula).fit()  # logistic regression
        else:
            model = sm.ols(data=self.df, formula=formula).fit()  # linear regression

        return model

    def multiple_regression(self, kind: str, x_cols, y_col):
        """
        function for performing a simple regression

        Parameters
        ----------
        kind
            kind of regression (linear or logistic)
        x_cols
            column names of x
        y_col
            column name of y
        Returns
        -------
        model
            regression model

        """
        column_check = [x for x in x_cols if x in self.df.columns]
        if not column_check or y_col not in self.df.columns:
            raise KeyError('columns do not exist')

        x_formula = "+".join(x_cols)

        formula = f"{y_col}~{x_formula}"
        if kind == "logistic":
            # check if values for y are all between 0 and 1
            between = self.df[y_col].between(0, 1).all()
            if not between:
                raise ValueError(f'values of {y_col} are not between 0 and 1')
            model = sm.mnlogit(data=self.df, formula=formula).fit()  # logistic regression
        else:
            model = sm.ols(data=self.df, formula=formula).fit()  # linear regression

        return model

    def hypothesis_test(self, hypothesis):
        """
        function for performing a hypothesis test

        Parameters
        ----------
        hypothesis
            is the hypothesis

        Returns
        -------
        answer
            answer of hypothesis

        """
        if hypothesis is None:
            raise HypothesisError("no valid hypothesis")

        if "corresponds to the population" in hypothesis:
            func = self.one_sample_test
        elif "are equal" in hypothesis:
            func = self.two_sample_test
        elif "there is a difference between" in hypothesis:
            func = self.paired_sample_test
        elif "are independent" in hypothesis:
            func = self.chi_squared_test
        else:
            raise HypothesisError("no valid hypothesis")
        return func(hypothesis)

    def one_sample_test(self, hypothesis):
        """
        function for performing one sample test

        Parameters
        ----------
        hypothesis
            is the hypothesis

        Returns
        -------
        answer
            answer of hypothesis
        """
        # hypothesis: {attr} corresponds to the population
        hypothesis_split = hypothesis.split(" ")
        col = hypothesis_split[0].lower()

        alt_hypothesis = f"{col} does not corresponds to the population"
        tscore, pval = stats.ttest_1samp(a=self.df[col], popmean=self.df[col].mean())
        answer = alt_hypothesis if pval < 0.05 else hypothesis
        return answer

    def two_sample_test(self, hypothesis):
        """
        function for performing a two sample test

        Parameters
        ----------
        hypothesis
            is the hypothesis
        Returns
        -------
        answer
            answer of hypothesis
        """
        # hypothesis: {attr_1} and {attr_2} are equal
        hypothesis_split = hypothesis.split(" ")
        col1 = hypothesis_split[0].lower()
        col2 = hypothesis_split[2].lower()

        alt_hypothesis = f"{col1} and {col2} are not equal"
        tscore, pval = stats.ttest_ind(a=self.df[col1], b=self.df[col2], equal_var=False)
        answer = alt_hypothesis if pval < 0.05 else hypothesis
        return answer

    def paired_sample_test(self, hypothesis):
        """
        function for performing a paired sample test

        Parameters
        ----------
        hypothesis
            is the hypothesis
        Returns
        -------
        answer
            answer of hypothesis
        """
        # hypothesis: There is a difference between {attr_1} and {attr_2}
        hypothesis_split = hypothesis.split(" ")
        before = hypothesis_split[-3].lower()
        after = hypothesis_split[-1].lower()

        alt_hypothesis = f"There is not a difference between {before} and {after}"
        tscore, pval = stats.ttest_rel(a=self.df[before], b=self.df[after])
        answer = alt_hypothesis if pval < 0.05 else hypothesis
        return answer

    def chi_squared_test(self, hypothesis):
        """
        function for performing a chi squared test

        Parameters
        ----------
        hypothesis
            is the hypothesis
        Returns
        -------
        answer
            answer of hypothesis
        """
        # hypothesis: {attr_1} and {attr_2} are independent
        hypothesis_split = hypothesis.split(" ")
        col1 = hypothesis_split[0].lower()
        col2 = hypothesis_split[2].lower()

        alt_hypothesis = f"{col1} and {col2} are not independent"

        ct = pd.crosstab(self.df[col1], self.df[col2])
        chi, pval, dof, exp = stats.chi2_contingency(ct)
        answer = alt_hypothesis if pval < 0.05 else hypothesis
        return answer

    def lorenz_curve(self, colname: str = None, title: str = None):
        """
        function for calculating, visualize and save the lorenz curve

        Parameters
        -------
        colname
            is the column which should be selected for the lorenz curve
        title
            [optional] title for plot


        Returns
        -------
        fig
            lorenz curve which is created
        """

        df = self.df
        col = df[colname]

        df = np.asarray(col)
        sorted_df = np.sort(df)
        y = (sorted_df / sorted_df.sum()).cumsum()
        n = df.shape[0]
        x = np.arange(1, n + 1) / n

        fig, ax = plt.subplots()
        ax.plot(x, y, label='Lorenz Curve')
        ax.plot((0, 1), (0, 1), color='r', label='Perfect Equality')
        ax.legend()
        ax.set_title(title)

        return fig
