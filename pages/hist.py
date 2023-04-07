from dash import dcc, html
import dash_bootstrap_components as dbc

radio_options = [
    {'label': 'age/bmi/charges', 'value': 'age bmi charges'},
    {'label': 'sex/region/children/smoker', 'value': 'sex region children smoker'}
]

dropdown_full_options = [
    {'label': 'Histogram', 'value': 'Histogram'},
    {'label': 'Curv + Rug plot', 'value': 'Distplot'},
]

dropdown_only_hist_options = [
    {'label': 'Histogram', 'value': 'Histogram'}
]

graf_hidden = {
    "display": "none"
}

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

hist_page = [
    html.Div(
        children=[
            html.H1(id='hist_page_title', children='Histograms', className='header-title',
                    style={'textAlign': 'center'})
        ], className='header'),

    dbc.RadioItems(id='hist_page_radio',
                   options=radio_options,
                   value='age bmi charges',
                   style=radio_items,
                   inline=False),

    dcc.Dropdown(id='hist_page_drop',
                 options=dropdown_full_options,
                 value='Histogram', className="dropdown"
                 ),

    html.Div([
        dcc.Graph(id='graph_4_1', className="card", style=graf_flex),
        dcc.Graph(id='graph_4_2', className="card", style=graf_flex),
    ], style=div_flex),

    html.Div([
        dcc.Graph(id='graph_4_3', className="card", style=graf_flex),
        dcc.Graph(id='graph_4_4', className="card", style=graf_flex),
    ], style=div_flex)

    # dcc.Graph(id='graph2',
    #           figure=px.scatter(df, x='age',
    #                             y='charges', facet_col='smoker'), className="card")
]
# , style={"display": "flex"}
