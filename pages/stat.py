from dash import html, dcc
import dash_bootstrap_components as dbc

switch_stat_table_options = [
    {"label": "Show statistic table?", "value": False}
]

switch_view_table_options = [
    {"label": "Show table?", "value": False}
]

checklist_stat_table_options = [
    {"label": "Age", "value": "age"},
    {"label": "BMI", "value": "bmi"},
    {"label": "Charges", "value": "charges"}
]

checklist_view_table_options = [
    {"label": "Sex", "value": "sex"},
    {"label": "Smoker", "value": "smoker"},
    {"label": "Region", "value": "region"},
    {"label": "Age", "value": "age"},
    {"label": "BMI", "value": "bmi"},
    {"label": "Charges", "value": "charges"},
    {"label": "Children", "value": "children"}
]

div_off = {
    "display": "none"
}

div_on = {
    "display": "block"
}

div_flex = {
    "display": "flex",
    "alignItems": "center"
}

div_jstf = {
    "display": "flex",
    "alignItems": "center",
    "justify-content": "space-between"
}

dropdown_menu_items_params = [
    dbc.DropdownMenuItem("sex", id="dropdown_button_sex", n_clicks=0),
    dbc.DropdownMenuItem("smoker", id="dropdown_button_smoker", n_clicks=0),
    dbc.DropdownMenuItem("region", id="dropdown_button_region", n_clicks=0),
    dbc.DropdownMenuItem("age", id="dropdown_button_age", n_clicks=0),
    dbc.DropdownMenuItem("bmi", id="dropdown_button_bmi", n_clicks=0),
    dbc.DropdownMenuItem("charges", id="dropdown_button_charges", n_clicks=0),
    dbc.DropdownMenuItem("children", id="dropdown_button_children", n_clicks=0),
]

dropdown_menu_items_for_numb = [
    {"label": "=", "value": "=="},
    {"label": "!=", "value": "!="},
    {"label": ">", "value": ">"},
    {"label": ">=", "value": ">="},
    {"label": "<", "value": "<"},
    {"label": "<=", "value": "<="},
]

dropdown_menu_items_for_categorial = [
    {"label": "=", "value": "=="},
    {"label": "!=", "value": "!="},
    {"label": "in", "value": "in"},
    {"label": "not in", "value": "not in"},
]

dropdown_menu_and_or = [
    {"label": "AND", "value": "&"},
    {"label": "OR", "value": "|"}
]

input_style_10rem = {
    "width": "10rem"
}

input_style_6rem = {
    "width": "6rem"
}

button_style_5rem = {
    "width": "5rem"
}

button_style_update = {
    "width": "5rem",
    "margin-left": "20.75rem"
}

dropdown_numb_options = [
    {'label': 'Age', 'value': 'age'},
    {'label': 'BMI', 'value': 'bmi'},
    {'label': 'Charges', 'value': 'charges'},
    {'label': 'Children', 'value': 'children'}
]

dropdown_categ_options = [
    {'label': 'Sex', 'value': 'sex'},
    {'label': 'Smoker', 'value': 'smoker'},
    {'label': 'Region', 'value': 'region'}
]

stat_page = [
    html.Div(
        children=[
            html.H1(id='stat_page_title', children='Statistic', className='header-title',
                    style={'textAlign': 'center'})
        ], className='header'),

    dbc.Checklist(id="view_table_switch", options=switch_view_table_options, value=False, switch=True),
    html.Div([
        dbc.Checklist(id="view_table_check", options=checklist_view_table_options, inline=True),
        html.Div([
            html.Div([
                dcc.Dropdown(id="view_table_criterion_numb_1", className="dropdown",
                             options=dropdown_numb_options, style=input_style_10rem),
                dcc.Dropdown(id="view_table_dropdown_menu_symbol_numb_1", className="dropdown",
                             options=dropdown_menu_items_for_numb, style=input_style_10rem),
                dbc.Input(style=input_style_10rem, id="view_table_param_numb_1"),
                dbc.FormText(id="view_table_criterion_numb_help_1")
            ], style=div_flex),
            # # #

            dcc.Dropdown(id="view_table_dropdown_menu_logic_1", className="dropdown", value=None,
                         options=dropdown_menu_and_or, style=input_style_6rem),

            # # #
            html.Div([
                dcc.Dropdown(id="view_table_criterion_numb_2", className="dropdown", value=None,
                             options=dropdown_numb_options, style=input_style_10rem),
                dcc.Dropdown(id="view_table_dropdown_menu_symbol_numb_2", className="dropdown", value=None,
                             options=dropdown_menu_items_for_numb, style=input_style_10rem),
                dbc.Input(style=input_style_10rem, id="view_table_param_numb_2", valid=False),
                dbc.FormText(id="view_table_criterion_numb_help_2")
            ], style=div_flex),
            # # #

            dcc.Dropdown(id="view_table_dropdown_menu_logic_2", className="dropdown", value=None,
                         options=dropdown_menu_and_or, style=input_style_6rem),

            # # #
            html.Div([
                dcc.Dropdown(id="view_table_criterion_categ_1", className="dropdown", value=None,
                             options=dropdown_categ_options, style=input_style_10rem),
                dcc.Dropdown(id="view_table_dropdown_menu_symbol_categ_1", className="dropdown", value=None,
                             options=dropdown_menu_items_for_categorial, style=input_style_10rem),
                dcc.Dropdown(id="view_table_dropdown_menu_categ_params", className="dropdown", value=None, multi=True,
                             style=input_style_10rem)
                # dbc.Input(style=input_style_10rem, id="view_table_param_categ_1", valid=True),
            ], style=div_flex),
            html.Div([
                dbc.Button("Clear", id="view_table_clear_button", outline=True, color="primary",
                           n_clicks=0, style=button_style_5rem),
                dbc.Button("Update", id="view_table_update_button", outline=True, color="success",
                           n_clicks=0, style=button_style_update),
            ]),
        ]),
        html.Div([
            dbc.FormText("Number of lines"),
            dbc.Input(id="page_size_view_table", type="number", value=10, style=input_style_6rem, size="sm", min=1),
            dbc.FormText(id="view_table_total_lines"),
        ]),
        html.Div([
            dbc.FormText("Current page"),
            dbc.Input(id="page_cur_view_table", type="number", style=input_style_6rem, size="sm", value=1, min=1),
            dbc.FormText(id="view_table_total_pages"),
        ]),
        dbc.Table(id="view_table", children=None, bordered=True)
    ], id="view_table_div", style=div_on),

    dbc.Checklist(id="stat_table_switch", options=switch_stat_table_options, value=False, switch=True),
    html.Div([
        dbc.Checklist(id="stat_table_check", options=checklist_stat_table_options, inline=True),
        dbc.Table(id="stat_table", children=None, bordered=True)
    ], id="stat_table_div", style=div_on)
]
