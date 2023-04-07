from numpy import quantile
from dash import html
from abc import ABC, abstractmethod


class Table(ABC):
    _table_header = None
    _table_body = None

    def __init__(self):
        self._table = None
        self._rows = []

    @property
    def table(self):
        if not self._table:
            self._generate_row()
            self._generate_body()
            self._table = self._table_header + self._table_body
        return self._table

    @abstractmethod
    def _generate_row(self):
        pass

    @abstractmethod
    def _generate_body(self):
        pass


class TableStat(Table):
    _table_header = [
        html.Thead(html.Tr([html.Th("Имя"),
                            html.Th("Среднее"),
                            html.Th("Медиана"),
                            html.Th("Станд. отклонение"),
                            html.Th("Межквартильный размах"),
                            html.Th("Верхняя квартиль"),
                            html.Th("Нижняя квартиль"),
                            html.Th("Коэффициент ассиметрии"),
                            html.Th("Коэффициент эксцесса"),
                            html.Th("Количество наблюдений"),
                            html.Th("Количество пропущенных значений")]))
    ]

    def __call__(self, df, row_names: list):
        self.df = df
        self.row_names = row_names
        self._rows = []
        self._table = None
        return self

    @staticmethod
    def _quantity(x):
        quartiles = quantile(x, [0.25, 0.75])
        return quartiles[1] - quartiles[0]

    def _ds(self, name, param):
        return self.df[name].describe()[param]

    def _generate_row(self):
        for name in self.row_names:
            row = html.Tr([html.Td(name.capitalize()),
                           html.Td(self.df[name].mean()),
                           html.Td(self.df[name].median()),
                           html.Td(self._ds(name, 'std')),
                           html.Td(self._quantity(self.df[name])),
                           html.Td(self._ds(name, '75%')),
                           html.Td(self._ds(name, '25%')),
                           html.Td(self.df[name].skew()),
                           html.Td(self.df[name].kurtosis()),
                           html.Td(self._ds(name, 'count')),
                           html.Td(self.df[name].isnull().sum())])
            self._rows.append(row)

    def _generate_body(self):
        self._table_body = [html.Tbody(self._rows)]


class TableView(Table):
    def __call__(self, df, col_names, count_rows=10, logic=None):
        self._rows = []
        self._table = None
        self.df = df
        self.col_names = ['id'] + col_names
        self.count_rows = count_rows
        self._generate_head()
        return self

    def _generate_head(self):
        self._table_header = [html.Thead(html.Tr([html.Th(col_name) for col_name in self.col_names]))]

    def _generate_row(self):
        # for i in range(self.count_rows):
        for i in range(len(self.df)):
            one_row = [html.Td(self.df.iloc[i].name)]
            for col_name in self.col_names[1:]:
                one_row.append(html.Td(self.df[col_name].iloc[i]))
            self._rows.append(html.Tr(one_row))

    def _generate_body(self):
        self._table_body = [html.Tbody(self._rows)]
