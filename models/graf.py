from plotly.express import histogram, box, scatter
from plotly.figure_factory import create_distplot
from abc import ABC, abstractmethod


class Graf(ABC):
    def __init__(self):
        self._plots = []

    def __call__(self, df, columns: list = None, x=None, y=None, color=None):
        self.df = df
        self.columns = columns
        self.x = x
        self.y = y
        self.color = color
        self._plots = []
        return self

    @property
    def plots(self) -> list:
        if not self._plots:
            self._plots = self._gen_plots(self.columns)
        return self._plots

    @abstractmethod
    def _gen_plots(self, columns: list = None):
        pass


class Hist(Graf):
    def _gen_plots(self, columns: list = None):
        return [histogram(self.df, x=column, histfunc='count') for column in columns]


class Dist(Graf):
    def _gen_plots(self, columns: list = None):
        return [create_distplot([self.df[column]], [column], show_hist=False)
                for column in columns]


class Box(Graf):
    def _gen_plots(self, columns: list = None):
        return [box(self.df, x=self.x, y=self.y, color=self.color, notched=True)]


class Scatter(Graf):
    def _gen_plots(self, columns: list = None):
        return [scatter(self.df, x=self.x, y=self.y, color=self.color)]


class Bar(Graf):
    def _gen_plots(self, columns: list = None):
        return [histogram(self.df, x=self.x, color=self.color, histfunc='count')]
