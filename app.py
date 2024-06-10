import sys
import os
from dash import Dash, Output, Input, State, html
from app_components.sample_word import sample_word
from app_components.components import *
from src.worker import convert


# app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = "Hangul to IPA"

# layout
app.layout = html.Div(
    [
        donation_ribbon,
        header,
        dbc.Label("Enter your 한글:"),
        dbc.Input(id='hangul-input', placeholder=sample_word, type='text'),
        dbc.FormText("Type something in the box above. Upon launching, a random word sill appear",
                     className='mb-5'),
        html.Br(),
        html.Br(),
        dbc.ButtonGroup(
            [
                dbc.Button(
                    "Convert",
                    id="convert-btn",
                    className='mb-3',
                    color='primary'
                ), dbc.Button(
                    "Settings",
                    id='settings-btn',
                    className='mb-3',
                    color='secondary',
                    n_clicks=0
                )
            ],
            className="me-1",
        ),
        dbc.Card(
            [
                dbc.Row([
                        dbc.Label("Your input:", style={'fontWeight': 'bold'}),
                        dbc.Textarea(
                            id='echo-input',
                            value='',
                            style={'width': '100%'},
                            readOnly=True
                        ),
                        ],
                        id='echo-input-row',
                        className='mb-3'
                        ),
                dbc.Row(
                    [
                        dbc.Label("", style={'fontWeight': 'bold'}, id='output-label'),
                        dbc.Textarea(
                            id='result-box',
                            value='',
                            style={'width': '100%'},
                            readOnly=True
                        ),
                    ],
                    id='output-row'

                ),
            ],
            body=True,
            id="output",
            className='mb-3'
        ),
        dbc.Collapse(
            dbc.Card(
                [
                    dbc.Label("What do you want to do?", style={'fontWeight': 'bold'}),
                    dbc.RadioItems(
                        options=[
                            {"label": "IPA Transcription", "value": "ipa"},
                            {"label": "Yale Romanization", "value": "yale"},
                        ],
                        value='ipa',
                        id="ipa-yale",
                        className="mb-4"
                    ),
                    dbc.Label("Phonological rules", style={'fontWeight': 'bold'}),
                    dbc.Row(ipa_parameters, id='transcription_settings', className='mb-3'),
                ],
                body=True),
            id="settings",
            is_open=False,
        ),
    ],
    style={'padding': '10px'}
)


@app.callback(
    Output("settings", "is_open"),
    [Input("settings-btn", "n_clicks")],
    [State("settings", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output('transcription_settings', 'children'),
    [Input('ipa-yale', 'value')]
)
def update_transcription_settings(selected_value):
    if selected_value == 'ipa':
        return ipa_parameters
    elif selected_value == 'yale':
        return yale_parameters
    return html.Div()  # Return an empty div if no option is selected


@app.callback(
    [Output("echo-input", "value"),
     Output("output-label", "children"),
     Output("result-box", "value")],
    [Input("hangul-input", "value"),
     Input("hangul-input","placeholder"),
     Input('ipa-yale', 'value'),
     Input("parameter-checklist", "value")],
)
def transcribe(usr_input, placeholder, convention, rules):
    to_convert = usr_input if usr_input is not None else placeholder
    applying_rules = ''.join(rules)
    result = convert(hangul=to_convert,
                     rules_to_apply=applying_rules,
                     convention=convention,
                     sep='.')
    result_label = f'Your {convention.upper()} output:'
    return to_convert, result_label, result

if __name__ == "__main__":
    app.run_server(debug=True)



# app.layout = html.Div([
#     html.H1("Dash App Example"),
#     dcc.Input(
#         id='hangul-input',
#         type='text',
#         placeholder=sample_word
#     ),
#     html.Br(),
#     dcc.Checklist(
#         id='rule-checklist',
#         options=[{'label': rule['name'], 'value': rule['code']} for rule_set in all_rules.values() for rule in rule_set],
#         value=[]
#     ),
#     html.Br(),
#     html.Button('Submit', id='submit-button', n_clicks=0),
#     html.Div(id='output-container', children=[])
# ])
#
# @app.callback(
#     Output('output-container', 'children'),
#     Input('submit-button', 'n_clicks'),
#     State('hangul-input', 'value'),
#     State('rule-checklist', 'value')
# )
# def update_output(n_clicks, selected_sample, selected_rules):
#     if n_clicks > 0:
#         # Processing logic here
#         # This is a placeholder for the actual processing based on selected_sample and selected_rulesll
#         processed_data = f"Processed {selected_sample} with rules {selected_rules}"
#         return html.Div([
#             html.H2("Processed Output"),
#             html.P(processed_data)
#         ])
#     return ""
#
#