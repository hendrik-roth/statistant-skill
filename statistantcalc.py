import pandas as pd


class StatistantCalc:
    def __init__(self, df):
        self.df = df

    def mean(self, col):
        mean = round(self.df[col].mean(), 3)
        return mean

    def mean_interval(self, lower, upper, col):
        if lower > upper:
            lower, upper = upper, lower
        mean = round(self.df.loc[self.df.index[(lower - 1):upper], col].mean(), 3)
        return mean

    def mean_2_cells(self, val1, val2, col):
        mean = round(self.df.loc[self.df.index[[val1 - 1, val2 - 1]], col].mean(), 3)
        return mean
