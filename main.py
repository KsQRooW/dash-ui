from dash.dependencies import Input, Output, State
from math import ceil

from pages import *
from settings import app, df_uploaded, df, df_no_cat, form_df_not_cat
from models import hist, dist, box, scatter, bar, stat_table, view_table, logic


_ = None
app.layout = sidebar

# # # Navigating # # #


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    prevent_initial_call=True
)
def pagecontent(pathname):
    """
    Navbar, навигация приложения.
    В случае, если файл не был приложен - навигация не будет отображать контент.

    :param pathname: имя эндпоинта (из url'а)
    """
    if df_uploaded.get('file'):
        global df, df_no_cat
        df = df_uploaded['df']
        df_no_cat = form_df_not_cat(df)
        if pathname == "/hist":
            return hist_page

        elif pathname == "/box_whisk":
            return box_whisk_page

        elif pathname == "/scatter":
            return scatter_page

        elif pathname == "/bar":
            return bar_page

        elif pathname == "/stat":
            return stat_page


# # # Histogram # # #


@app.callback(
    [Output('graph_4_1', 'figure'),
     Output('graph_4_2', 'figure'),
     Output('graph_4_3', 'figure'),
     Output('graph_4_4', 'figure'),
     Output('hist_page_title', 'children'),
     Output("page_hist_loading", "children"),
     Output('graph_4_3', 'style'),
     Output('graph_4_4', 'style')],
    [Input('hist_page_drop', 'value'),
     Input('hist_page_radio', 'value')]
)
def hist_page_interface(value: str, cols: str):
    """
    Отображение графиков на странице "Histograms".

    :param value: значение из dropdown
    :param cols: значение из radio buttons
    """

    res = []
    title = ''
    styles = [graf_flex, graf_flex]

    cols = cols.split()

    if value == 'Histogram':
        res = hist(df, cols).plots
        title = 'Histogram'

    elif value == 'Distplot':
        res = dist(df_no_cat, cols).plots
        title = 'Curv + Rug plot'

    # FIXME: забито гвоздями на 3 или 4 графика
    if len(res) == 3:
        res.append(res[0])
        styles = [graf_flex, graf_hidden]

    return *res, title, _, *styles


@app.callback(
    [Output("hist_page_drop", "options"),
     Output("hist_page_drop", "value")],
    Input('hist_page_radio', 'value')
)
def hist_page_radio_rules(value):
    """
    Логика отображения текста в dropdown на странице "Histograms"

    :param value: значение из radio button
    """
    if value == "sex region children smoker":
        return dropdown_only_hist_options, "Histogram"
    elif value == "age bmi charges":
        return dropdown_full_options, "Histogram"


# # # Box # # #


@app.callback(
    [Output("graph_3_1", "figure"),
     Output("page_box_whisk_loading", "children")],
    [Input("box_whisk_radio_y", "value"),
     Input("box_whisk_radio_x", "value"),
     Input("box_whisk_radio_category_color", "value")]
)
def box_whisk_page_interface(y, x, color):
    """
    Отображение графика на странице Box-And-Whiskers

    :param y: значение из radio button "... for Y-axis"
    :param x: значение из radio button "... for X-axis"
    :param color: значение radio button "Category group?", для группировки по цвету
    """
    res = box(df=df, y=y, x=x, color=color).plots[0]
    return res, _


@app.callback(
    Output("box_whisk_radio_category_color", "options"),
    Output("box_whisk_radio_category_color", "value"),
    Input("box_whisk_checklist", "value")
)
def box_whisk_page_category_group_show(value):
    """
    Отвечает за отображение radio button для группировки по категориям ("Category group?") для графика Box-And-Whisker

    :param value: True или False (True = необходимо отобразить radio button для группировки)
    """
    if value:
        return radio_options_category, None
    return radio_options_category_disabled, None


# # # Scatter # # #


@app.callback(
    [Output("graph_1_1", "figure"),
     Output("page_scatter_loading", "children")],
    [Input("scatter_radio_y", "value"),
     Input("scatter_radio_x", "value"),
     Input("scatter_radio_category_color", "value")]
)
def scatter_page_interface(y, x, color):
    """
    Отображение графика на странице Scatter

    :param y: значение из radio button "... for Y-axis"
    :param x: значение из radio button "... for X-axis"
    :param color: значение radio button "Category group?", для группировки по цвету
    """
    res = scatter(df=df, y=y, x=x, color=color).plots[0]
    return res, _


@app.callback(
    Output("scatter_radio_category_color", "options"),
    Output("scatter_radio_category_color", "value"),
    Input("scatter_checklist", "value")
)
def scatter_page_category_group_show(value):
    """
    Отвечает за отображение radio button для группировки по категориям ("Category group?") для графика Scatter

    :param value: True или False (True = необходимо отобразить radio button для группировки)
    """
    if value:
        return radio_options_full, None
    return radio_options_full_disabled, None


# # # Bar # # #


@app.callback(
    [Output("graph_2_1", "figure"),
     Output("page_bar_loading", "children")],
    [Input("bar_radio_x", "value"),
     Input("bar_radio_category_color", "value")]
)
def bar_page_interface(x, color):
    """
    Отображение графика на странице Bar

    :param x: значение из radio button "... for X-axis"
    :param color: значение radio button "Category group?", для группировки по цвету
    """
    res = bar(df=df, x=x, color=color).plots[0]
    return res, _


@app.callback(
    Output("bar_radio_category_color", "options"),
    Output("bar_radio_category_color", "value"),
    Input("bar_checklist", "value")
)
def bar_page_category_group_show(value):
    """
    Отвечает за отображение radio button для группировки по категориям ("Category group?") для графика Bar

    :param value: True или False (True = необходимо отобразить radio button для группировки)
    """
    if value:
        return radio_options_part, None
    return radio_options_part_disabled, None


# # # Statistic # # #


@app.callback(
    Output("stat_table_div", "style"),
    Input("stat_table_switch", "value")
)
def show_stat_table(value):
    """
    Отображение таблицы со статистикой по полям из датасета

    :param value: True или False (True = отобразить таблицу и поля для фильтрации)
    """
    if value:
        return div_on
    return div_off


@app.callback(
    [Output("stat_table", "children"),
     Output("page_stat_loading", "children")],
    Input("stat_table_check", "value")
)
def update_stat_table(value):
    """
    Обновление полей в таблице со статистикой

    :param value: значения, отмеченные на checkbox'ах, по которым будет отображаться статистика в таблице
    """
    if value:
        return stat_table(df, value).table, _
    return _, _


@app.callback(
    Output("view_table_div", "style"),
    Input("view_table_switch", "value")
)
def show_view_table(value):
    """
    Отображение полей для фильтрации и исходных данных датасета

    :param value: True или False (True = отобразить поля для фильтрации и таблицу с исходными данными датасета)
    """
    if value:
        return div_on
    return div_off


def validate_current_page(cur_numb, max_):
    """
    Вычисляем количество отображаемых строк в таблице с полями из датасета

    :param cur_numb: число, указанное в поле "Number of lines"
    :param max_: максимальное число строк в датасете
    :return: возвращает наименьшее из чисел cur_numb и max_
    """
    if cur_numb > max_:
        return max_
    return cur_numb


@app.callback(
    Output("view_table", "children"),
    Output("view_table_total_lines", "children"),
    Output("view_table_total_pages", "children"),
    Output("page_size_view_table", "max"),
    Output("page_cur_view_table", "max"),
    Output("page_size_view_table", "value"),
    Output("page_cur_view_table", "value"),

    Input("view_table_check", "value"),
    Input("page_size_view_table", "value"),
    Input("page_cur_view_table", "value"),
    Input("view_table_update_button", "n_clicks"),

    State("view_table_criterion_numb_1", "value"),
    State("view_table_dropdown_menu_symbol_numb_1", "value"),
    State("view_table_param_numb_1", "value"),
    State("view_table_dropdown_menu_logic_1", "value"),
    State("view_table_criterion_numb_2", "value"),
    State("view_table_dropdown_menu_symbol_numb_2", "value"),
    State("view_table_param_numb_2", "value"),
    State("view_table_dropdown_menu_logic_2", "value"),
    State("view_table_criterion_categ_1", "value"),
    State("view_table_dropdown_menu_symbol_categ_1", "value"),
    State("view_table_dropdown_menu_categ_params", "value")
)
def update_view_table_v2(value, page_size, page_current, _n_clicks,
                         name_numb_1, symbol_numb_1, val_numb_1, logic_1,
                         name_numb_2, symbol_numb_2, val_numb_2, logic_2,
                         name_categ_1, symbol_categ_1, val_categ_1):
    """
    Обновление отображаемых полей датасета с учетом пагинаций и логических условий (отобранных из нескольких строк
    dropdown и input-полей на странице)

    :param value: True или False (True = отображать таблицу с данными датасета)
    :param page_size: выбранное количество строк для отображения на странице в input-поле "Number of lines"
                      (используется для реализации пагинаций)
    :param page_current: текущая страница данных (связано с page_size, используется для реализации пагинаций)
    :param _n_clicks: сигнал о том, что была нажата кнопка "Update"
    :param name_numb_1: имя столбца с числовым признаком из 1-ой строки, 1-ого dropdown блока
    :param symbol_numb_1: логическая операция сравнения из 1-ой строки, 2-ого dropdown блока
    :param val_numb_1: числовое значение, для сопоставления с ним поля name_numb_1 с помощью логического оператора
                       symbol_numb_1
    :param logic_1: 1-ая логическая операция типа "OR" или "AND", для связывания логических условий
    :param name_numb_2: имя столбца с числовым признаком из 2-ой строки, 1-ого dropdown блока
    :param symbol_numb_2: логическая операция сравнения из 2-ой строки, 2-ого dropdown блока
    :param val_numb_2: числовое значение, для сопоставления с ним поля name_numb_2 с помощью логического оператора
                       symbol_numb_2
    :param logic_2: 2-ая логическая операция типа "OR" или "AND", для связывания логических условий
    :param name_categ_1: имя столбца с категориальным признаком из 3-ой строки, 1-ого dropdown блока
    :param symbol_categ_1: логическая операция сравнения из 3-ой строки, 2-ого dropdown блока
    :param val_categ_1: категориальное значение, для сопоставления с ним поля name_categ_1 с помощью логического
                        оператора symbol_numb_2
    """
    # FIXME: забил гвоздями на 3 выражения (сам метод целиком в том числе)
    logic(expr=(name_numb_1, symbol_numb_1, val_numb_1))
    logic(expr=(name_numb_2, symbol_numb_2, val_numb_2))
    logic(expr=(name_categ_1, symbol_categ_1, val_categ_1))
    logic(and_or_symbol=(logic_1, logic_2), clear=True)

    expr = logic.full_expr
    expr = expr.replace(logic.mask, "df")

    max_len = len(df)
    page_size = validate_current_page(page_size, max_len or 1)

    if value:
        sorted_df = eval(f"df[{expr}]") if expr else df
        max_len = len(sorted_df)

        page_current = validate_current_page(page_current, ceil(max_len / page_size) or 1)

        small_df = sorted_df[(page_current - 1) * page_size:page_current * page_size]

        res = (
            view_table(small_df, value).table,
            f"total: {max_len}",
            f"last: {ceil(max_len / page_size)}",
            max_len or 1,
            ceil(max_len / page_size) or 1,
            page_size,
            page_current
        )
        return res
    res = (
        None,
        f"total: {max_len}",
        f"last: {ceil(max_len / page_size)}",
        max_len or 1,
        ceil(max_len / page_size) or 1,
        page_size,
        page_current
    )
    return res


@app.callback(
    Output("view_table_dropdown_menu_categ_params", "options"),
    Input("view_table_criterion_categ_1", "value")
)
def update_dropdown_categorical_options(name):
    """
    Возвращает в последний dropdown в третьей строке набор уникальных значений для категориального признака в датасете.
    Сам категориальный признак выбирается в этой же строке в 1-ом dropdown.

    :param name: имя категориального признака
    """
    if name:
        return df[name].unique()
    return []


@app.callback(
    Output("view_table_dropdown_menu_categ_params", "multi"),
    Input("view_table_dropdown_menu_symbol_categ_1", "value")
)
def update_dropdown_categorical_multi(val):
    """
    Обработчик логических условий "in" и "not in" в выпадающем списке в третьей строке для категориальных признаков

    :param val: значение из выпадающего списка с логическими операциями для категориальных признаков (3 строка)
    :return:
    """
    if val in ("in", "not in"):
        return True
    return False


@app.callback(
    Output("view_table_criterion_numb_help_1", "children"),
    Input("view_table_criterion_numb_1", "value")
)
def validate_numb_param_1(name):
    """
    Возвращает подсказку рядом с последним input-полем в первой строке параметров,
    которая показывает минимальное и максимальное значение для выбранного параметра (из выпадающего списка 1-ой строки)

    :param name: имя параметра из выпадающего списка (из второй строки параметров)
    """
    if name:
        return f"min: {df[name].min()}, max: {df[name].max()}"
    return None


@app.callback(
    Output("view_table_criterion_numb_help_2", "children"),
    Input("view_table_criterion_numb_2", "value")
)
def validate_numb_param_2(name):
    """
    Возвращает подсказку рядом с последним input-полем во второй строке параметров,
    которая показывает минимальное и максимальное значение для выбранного параметра (из выпадающего списка 2-ой строки)

    :param name: имя параметра из выпадающего списка (из первой строки параметров)
    """
    if name:
        return f"min: {df[name].min()}, max: {df[name].max()}"
    return None


@app.callback(
    Output("view_table_param_numb_1", "invalid"),
    Input("view_table_param_numb_1", "value")
)
def validate_input_1(value):
    """
    Валидация значения последнего input-поля в первой строке

    :param value: значение последнего input-поля из первой строки
    """
    if value:
        try:
            float(value)
            return False
        except ValueError:
            return True
    return False


@app.callback(
    Output("view_table_param_numb_2", "invalid"),
    Input("view_table_param_numb_2", "value")
)
def validate_input_2(value):
    """
    Валидация значения последнего input-поля во второй строке

    :param value: значение последнего input-поля из второй строки
    """
    if value:
        try:
            float(value)
            return False
        except ValueError:
            return True
    return False


# TODO: добавить кнопку Clear для очистки все параметров сортировки
@app.callback(
    Output("view_table_criterion_numb_1", "value"),
    Output("view_table_dropdown_menu_symbol_numb_1", "value"),
    Output("view_table_param_numb_1", "value"),
    Output("view_table_dropdown_menu_logic_1", "value"),
    Output("view_table_criterion_numb_2", "value"),
    Output("view_table_dropdown_menu_symbol_numb_2", "value"),
    Output("view_table_param_numb_2", "value"),
    Output("view_table_dropdown_menu_logic_2", "value"),
    Output("view_table_criterion_categ_1", "value"),
    Output("view_table_dropdown_menu_symbol_categ_1", "value"),
    Output("view_table_dropdown_menu_categ_params", "value"),

    Input("view_table_clear_button", "n_clicks")
)
def clear_all_inputs(_n_clicks):
    """
    Очистка всех input-полей по кнопке "Clear" для фильтрации таблицы датасета

    :param _n_clicks: сигнал нажатия
    """
    return [None] * 11


if __name__ == '__main__':
    app.run_server()
