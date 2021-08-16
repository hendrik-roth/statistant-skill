from .exceptions import FunctionNotFoundError


class StatistantCalc:
    def __init__(self, df):
        self.df = df
        self.selected = None

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
            "greatest value": df.max,
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
