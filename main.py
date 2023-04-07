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
    [Input("url", "pathname"),
     ],
    prevent_initial_call=True
)
def pagecontent(pathname):
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
     Output('graph_4_4', 'style')
     ],
    [Input('hist_page_drop', 'value'),
     Input('hist_page_radio', 'value')]
)
def hist_page_interface(value: str, cols: str):
    res = []
    title = ''
    styles = [graf_flex, graf_flex]

    cols = cols.split()
    # print(f"{value}: {cols}")  # Для отладки

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
    res = box(df=df, y=y, x=x, color=color).plots[0]
    return res, _


@app.callback(
    Output("box_whisk_radio_category_color", "options"),
    Output("box_whisk_radio_category_color", "value"),
    Input("box_whisk_checklist", "value")
)
def box_whisk_page_category_group_show(value):
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
    res = scatter(df=df, y=y, x=x, color=color).plots[0]
    return res, _


@app.callback(
    Output("scatter_radio_category_color", "options"),
    Output("scatter_radio_category_color", "value"),
    Input("scatter_checklist", "value")
)
def scatter_page_category_group_show(value):
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
    res = bar(df=df, x=x, color=color).plots[0]
    return res, _


@app.callback(
    Output("bar_radio_category_color", "options"),
    Output("bar_radio_category_color", "value"),
    Input("bar_checklist", "value")
)
def bar_page_category_group_show(value):
    if value:
        return radio_options_part, None
    return radio_options_part_disabled, None


# # # Statistic # # #


@app.callback(
    Output("stat_table_div", "style"),
    Input("stat_table_switch", "value")
)
def show_stat_table(value):
    if value:
        return div_on
    return div_off


@app.callback(
    [Output("stat_table", "children"),
     Output("page_stat_loading", "children")],
    Input("stat_table_check", "value")
)
def update_stat_table(value):
    if value:
        return stat_table(df, value).table, _
    return _, _


@app.callback(
    Output("view_table_div", "style"),
    Input("view_table_switch", "value")
)
def show_view_table(value):
    if value:
        return div_on
    return div_off


# @app.callback(
#     # Output("view_table", "children"),
#     Output("view_table", "columns"),
#     Output("view_table", "data"),
#     Input("view_table_check", "value"),
#     Input("view_table", "page_current"),
#     Input("view_table", "page_size")
# )
# def update_view_table(value, page_current, page_size):
#     if value:
#         # return view_table(df, value).table
#         columns = [{"name": i, "id": i} for i in value]
#         return columns, df[value][page_current * page_size:(page_current + 1) * page_size].to_dict('records')
#     return None, None
def validate_current_page(cur_numb, max):
    if cur_numb > max:
        return max
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
    # FIXME: забил гвоздями на 3 выражения (сам метод целиком в том числе)
    logic(expr=(name_numb_1, symbol_numb_1, val_numb_1))
    logic(expr=(name_numb_2, symbol_numb_2, val_numb_2))
    logic(expr=(name_categ_1, symbol_categ_1, val_categ_1))
    logic(and_or_symbol=(logic_1, logic_2), clear=True)

    expr = logic.full_expr
    expr = expr.replace(logic.mask, "df")
    print("INFO: logic_expr =", expr or None)

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
    if name:
        return df[name].unique()
    return []


@app.callback(
    Output("view_table_dropdown_menu_categ_params", "multi"),
    Input("view_table_dropdown_menu_symbol_categ_1", "value")
)
def update_dropdown_categorical_multi(val):
    if val in ("in", "not in"):
        return True
    return False


@app.callback(
    Output("view_table_criterion_numb_help_1", "children"),
    Input("view_table_criterion_numb_1", "value")
)
def validate_numb_param_1(name):
    if name:
        return f"min: {df[name].min()}, max: {df[name].max()}"
    return None


@app.callback(
    Output("view_table_criterion_numb_help_2", "children"),
    Input("view_table_criterion_numb_2", "value")
)
def validate_numb_param_2(name):
    if name:
        return f"min: {df[name].min()}, max: {df[name].max()}"
    return None


@app.callback(
    Output("view_table_param_numb_1", "invalid"),
    Input("view_table_param_numb_1", "value")
)
def validate_input_1(value):
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
    return [None] * 11


if __name__ == '__main__':
    app.run_server()
