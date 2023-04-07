import base64
import io
import os.path

from dash import Dash, Input, Output, State
import dash_bootstrap_components as dbc
from pandas import read_csv, read_excel


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
df_uploaded = {}


@app.callback(
    Output("modal_window_for_additional_button", "is_open"),
    Input("upload_file_button_hidden", "n_clicks"),
    prevent_initial_call=True
)
def upload_button(_n_clicks_):
    return True


@app.callback(
    Output("sidebar_input_symbol", "valid"),
    Output("sidebar_input_symbol", "invalid"),

    Output("uploaded_file_info", "value"),

    Input("upload_file_button_hidden", "n_clicks"),
    State("sidebar_input_path", "contents"),
    State("sidebar_input_path", "filename"),
    State("sidebar_input_symbol", "value"),
    prevent_initial_call=True
)
def input_file(_n_clicks, contents, filename, sep):
    global df
    valid = {
        "path": True if filename else False,
        "sep": True if sep else False
    }
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df_uploaded['df'] = read_csv(io.StringIO(decoded.decode('utf-8')), sep=sep)
    elif 'xls' in filename or 'xlsx' in filename:
        # Assume that the user uploaded an excel file
        df_uploaded['df'] = read_excel(io.BytesIO(decoded), 0)

    if filename and sep:
        df_uploaded['file'] = os.path.basename(filename)
        # return True, True, False, False, f"{os.path.basename(file)} // {sep}"
        return True, False, f"{os.path.basename(filename)} // {sep}"
    # return valid['path'], valid['sep'], not valid['path'], not valid['sep'], None
    return valid['sep'], not valid['sep'], None


def form_df_not_cat(df):
    df_no_cat = df.copy()

    changer_sex = {'female': 1, 'male': 2}
    df_no_cat['sex'] = df['sex'].map(lambda x: changer_sex[x])

    changer_smoker = {'no': 1, 'yes': 2}
    df_no_cat['smoker'] = df['smoker'].map(lambda x: changer_smoker[x])

    changer_region = {'northeast': 1, 'southwest': 2, 'northwest': 3, 'southeast': 4}
    df_no_cat['region'] = df['region'].map(lambda x: changer_region[x])
    return df_no_cat


df = read_csv(f'{os.getcwd()}\\assets\\insurance.csv', sep=',')
df_no_cat = form_df_not_cat(df)
