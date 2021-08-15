class StatistantCalc:
    def __init__(self, df):
        self.df = df

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
            "sum": df.sum,
        }

        result = round(function[func](), 3)
        return result

    def mean_2_cells(self, val1, val2, col):
        mean = round(self.df.loc[self.df.index[[val1 - 1, val2 - 1]], col].mean(), 3)
        return mean
