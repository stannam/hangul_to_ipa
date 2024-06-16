from dash import Dash, Output, Input, State, no_update
from app_components.components import *
from src.worker import convert, convert_many


# app
app = Dash(__name__,
           external_stylesheets=[
               dbc.themes.COSMO,
               'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css'
           ])
app.title = "Hangul to IPA"
server = app.server

# layout
app.layout = html.Div(
    [
        donation_ribbon,
        header,
        input_box,
        html.Br(),
        main_buttons,
        collapsed_parameter_setter,
        output_card,
        footer
    ],
    style={'padding': '10px'}
)


# callbacks

# click 'advanced' btn -> open collapsed settings card
@app.callback(
    Output("advanced", "is_open"),
    [Input("advanced-btn", "n_clicks")],
    [State("advanced", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# toggle between ipa and yale
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


# update separator example
@app.callback(
    [Output("sep-example", "children"),],
    [Input("separator", "value"),],
)
def show_sep_example(sep):
    example = f"Preview: {sep.join(['h', 'ɑ', 'ŋ', 'ɡ', 'ɯ', 'l'])}"
    return [example]


# the engine of this app. convert one word
@app.callback(
    [Output("echo-input", "children"),
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


# accept .txt file as a wordlist and convert many words
@app.callback(
    Output('download-processed-data', 'data'),
    [Input('upload-data', 'contents'),
     Input('ipa-yale', 'value'),
     Input("parameter-checklist", "value"),
     Input("separator", "value")
     ],
    [State('upload-data', 'filename'), State('upload-data', 'last_modified')],
    prevent_initial_call=True,
)
def transcribe_many(content, convention, rules, separator, name, date):
    if content is None:
        return no_update

    content_type, content_string = content.split(',')
    if 'text' not in content_type:
        return no_update

    rules = ''.join(rules)

    try:
        result = convert_many(long_content=content_string,
                              rules_to_apply=rules,
                              convention=convention,
                              sep=separator)
    except Exception as e:
        print(f"[DEBUG] {e}")
        return no_update

    if isinstance(result, int):
        # encountered error, typically file type not compitible
        return None
    return dict(content=result,
                filename=f'[CONVERTED] {name}')


if __name__ == "__main__":
    app.run_server(debug=True)
