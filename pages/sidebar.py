import os

from dash import dcc, html
import dash_bootstrap_components as dbc

SIDESTYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "2rem 1rem",
    "background-color": "#222222",
    "display": "flex",
    "flex-direction": "column",
    "justify-content": "space-between"
}

CONTSTYLE = {
    "margin-left": "18rem",
    "margin-right": "3rem",
    "padding": "2rem 1rem",
}

loader = {
    "width": "1rem"
}

navlink_flex = {
    "display": "flex",
    "alignItems": "center"
}

span_flex = {
    "flexGrow": "1"
}

hidden = {
    "display": "none"
}

modal_title_style = {
    "font-size": 18
}

button_width_15rem = {
    "width": "15rem"
}

href_style = {
    "color": "white",
    "text-decoration": "none"
}

sidebar = html.Div([
    dcc.Location(id="url"),
    html.Div(
        [
            html.Div([
                html.H6(html.A("Analyze", href="http://127.0.0.1:8050", style=href_style), className="display-3"),
                html.Hr(style={'color': 'white'}),
                dbc.Nav(
                    [
                        dbc.NavLink([html.Span("Histograms", style=span_flex),
                                     html.Div(dbc.Spinner(html.Div(id="page_hist_loading"), size="sm"), style=loader)],
                                    href="/hist", active="exact",
                                    style=navlink_flex),
                        dbc.NavLink([html.Span("Box-And-Whiskers", style=span_flex),
                                     html.Div(dbc.Spinner(html.Div(id="page_box_whisk_loading"), size="sm"),
                                              style=loader)],
                                    href="/box_whisk", active="exact",
                                    style=navlink_flex),
                        dbc.NavLink([html.Span("Scatter", style=span_flex),
                                     html.Div(dbc.Spinner(html.Div(id="page_scatter_loading"), size="sm"),
                                              style=loader)],
                                    href="/scatter", active="exact",
                                    style=navlink_flex),
                        dbc.NavLink([html.Span("Bar", style=span_flex),
                                     html.Div(dbc.Spinner(html.Div(id="page_bar_loading"), size="sm"), style=loader)],
                                    href="/bar", active="exact",
                                    style=navlink_flex),
                        dbc.NavLink([html.Span("Statistic", style=span_flex),
                                     html.Div(dbc.Spinner(html.Div(id="page_stat_loading"), size="sm"), style=loader)],
                                    href="/stat", active="exact",
                                    style=navlink_flex),
                    ],
                    vertical=True, pills=True),
            ]),
            html.Div([
                dbc.FormText("File name // Separator", id="input_for_uploaded_file"),
                dbc.Input(id="uploaded_file_info", size="sm", readonly=True),

                dbc.FormText("File path", id="sidebar_formtext_path"),
                # dbc.Input(id="sidebar_input_path", type="file", size="sm", valid=False),
                dcc.Upload(
                    id='sidebar_input_path',
                    children=html.Div([
                        'Select file',

                    ]), style={'borderStyle': 'dashed', 'color': "white", 'textAlign': 'center', 'borderWidth': '1px'}),


                dbc.FormText("Separator", id="sidebar_formtext_symbol"),
                dbc.Input(id="sidebar_input_symbol", size="sm", valid=False, value=','),



                dbc.Button("Загрузить файл", id="upload_file_button_hidden", color="primary", n_clicks=0, size="sm",
                           style=button_width_15rem)
            ])
        ],
        style=SIDESTYLE
    ),
    html.Div([
        html.Div(id="page-content", children=[], style=CONTSTYLE),
    ]),
])
