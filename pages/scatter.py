from dash import dcc, html
import dash_bootstrap_components as dbc

radio_options_category = [
    {"label": "Sex", "value": "sex"},
    {"label": "Smoker", "value": "smoker"},
    {"label": "Region", "value": "region"}
]

radio_options_category_disabled = [
    {"label": "Sex", "value": "sex", "disabled": True},
    {"label": "Smoker", "value": "smoker", "disabled": True},
    {"label": "Region", "value": "region", "disabled": True}
]

radio_options_numb = [
    {"label": "Age", "value": "age"},
    {"label": "BMI", "value": "bmi"},
    {"label": "Charges", "value": "charges"},
    {"label": "Children", "value": "children"}
]

radio_options_full = [
    {"label": "Sex", "value": "sex"},
    {"label": "Smoker", "value": "smoker"},
    {"label": "Region", "value": "region"},
    {"label": "Age", "value": "age"},
    {"label": "BMI", "value": "bmi"},
    {"label": "Charges", "value": "charges"},
    {"label": "Children", "value": "children"}
]

radio_options_full_disabled = [
    {"label": "Sex", "value": "sex", "disabled": True},
    {"label": "Smoker", "value": "smoker", "disabled": True},
    {"label": "Region", "value": "region", "disabled": True},
    {"label": "Age", "value": "age", "disabled": True},
    {"label": "BMI", "value": "bmi", "disabled": True},
    {"label": "Charges", "value": "charges", "disabled": True},
    {"label": "Children", "value": "children", "disabled": True}
]

checklist_options = [
    {"label": "Category group?", "value": False}
]

graf_flex = {
    "flex": "1"
}

radio_items = {
    "margin-top": "0.5rem",
    "margin-bottom": "0.5rem",
}

div_flex = {
    "display": "flex"
}

scatter_page = [
    html.Div(
        children=[
            html.H1(id='scatter_page_title', children='Scatter', className='header-title',
                    style={'textAlign': 'center'})
        ], className='header'),

    dbc.Label("Choose param for Y-axis"),
    dbc.RadioItems(
        id="scatter_radio_y",
        options=radio_options_numb,
        value="age"
    ),

    dbc.Label("Choose param for X-axis"),
    dbc.RadioItems(
        id="scatter_radio_x",
        options=radio_options_numb,
        value="bmi"
    ),

    # dbc.Label("Choose param for grouping"),
    dbc.Checklist(id="scatter_checklist", options=checklist_options, value=False, switch=True),
    dbc.RadioItems(
        id="scatter_radio_category_color",
        options=radio_options_category,
        inline=True
    ),

    html.Div([
        dcc.Graph(id='graph_1_1', className="card", style=graf_flex),
    ], style=div_flex),
]
