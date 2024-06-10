from dash import Dash, Output, Input, State, html
from app_components.sample_word import sample_word
from app_components.components import *
from src.worker import convert


# app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.title = "Hangul to IPA"
server = app.server

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
        collapsed_parameter_setter,
        output_card,

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
     Input("parameter-checklist", "value"),
     Input("separator", "value")],
)
def transcribe(usr_input, placeholder, convention, rules, separator):
    to_convert = usr_input if usr_input is not None else placeholder
    applying_rules = ''.join(rules)
    result = convert(hangul=to_convert,
                     rules_to_apply=applying_rules,
                     convention=convention,
                     sep=separator)
    result_label = f'Your {convention.upper()} output:'
    result = f'[{result}]' if convention == 'ipa' else result
    return to_convert, result_label, result


@app.callback(
    [Output("sep-example", "children"),],
    [Input("separator", "value"),],
)
def show_sep_example(sep):
    example = f"Preview: {sep.join(['h', 'ɑ', 'ŋ', 'ɡ', 'ɯ', 'l'])}"
    return [example]


if __name__ == "__main__":
    app.run_server(debug=True)
