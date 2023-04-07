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

box_whisk_page = [
    html.Div(
        children=[
            html.H1(id='box_whisk_page_title', children='Box-And-Whiskers diagram', className='header-title',
                    style={'textAlign': 'center'})
        ], className='header'),

    dbc.Label("Choose param for Y-axis"),
    dbc.RadioItems(
        id="box_whisk_radio_y",
        options=radio_options_numb,
        value="age"
    ),

    dbc.Label("Choose param for X-axis"),
    dbc.RadioItems(
        id="box_whisk_radio_x",
        options=radio_options_category,
        value="sex"
    ),

    # dbc.Label("Choose param for grouping"),
    dbc.Checklist(id="box_whisk_checklist", options=checklist_options, value=False, switch=True),
    dbc.RadioItems(
        id="box_whisk_radio_category_color",
        options=radio_options_category
    ),

    html.Div([
        dcc.Graph(id='graph_3_1', className="card", style=graf_flex),
    ], style=div_flex),
]
