from dash import dcc, html
import dash_bootstrap_components as dbc

radio_options_full = [
    {"label": "Sex", "value": "sex"},
    {"label": "Smoker", "value": "smoker"},
    {"label": "Region", "value": "region"},
    {"label": "Age", "value": "age"},
    {"label": "BMI", "value": "bmi"},
    {"label": "Charges", "value": "charges"},
    {"label": "Children", "value": "children"}
]

radio_options_part = [
    {"label": "Sex", "value": "sex"},
    {"label": "Smoker", "value": "smoker"},
    {"label": "Region", "value": "region"},
    {"label": "Children", "value": "children"}
]

radio_options_part_disabled = [
    {"label": "Sex", "value": "sex", "disabled": True},
    {"label": "Smoker", "value": "smoker", "disabled": True},
    {"label": "Region", "value": "region", "disabled": True},
    {"label": "Children", "value": "children", "disabled": True}
]

checklist_options = [
    {"label": "Category group?", "value": False}
]

graf_flex = {
    "flex": "1"
}

div_flex = {
    "display": "flex"
}

bar_page = [
    html.Div(
        children=[
            html.H1(id='bar_page_title', children='Bar', className='header-title',
                    style={'textAlign': 'center'})
        ], className='header'),

    dbc.Label("Choose param for X-axis"),
    dbc.RadioItems(
        id="bar_radio_x",
        options=radio_options_full,
        value="bmi"
    ),

    dbc.Checklist(id="bar_checklist", options=checklist_options, value=False, switch=True),
    dbc.RadioItems(
        id="bar_radio_category_color",
        options=radio_options_part,
        inline=True
    ),

    html.Div([
        dcc.Graph(id='graph_2_1', className="card", style=graf_flex),
    ], style=div_flex),
]