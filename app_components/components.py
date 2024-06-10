from dash import html
import dash_bootstrap_components as dbc


donation_ribbon = dbc.Stack([
        dbc.Alert(
                ["If you're enjoying it, please consider ",
                 html.A("buying me a coffee.",
                        href="https://buymeacoffee.com/linguisting",
                        target="_blank",
                        className="alert-link"),
                 ],
                id="alert-fade",
                color="secondary",
                dismissable=True,
                is_open=True,
                ),
        dbc.Alert(
            ["이 앱이 유익하다면 ",
             html.A("토스로 기부해주세요 (익명가능).",
                    href="https://toss.me/sleepywug",
                    target="_blank",
                    className="alert-link"),
             ],
            id="alert-fade-kor",
            color="secondary",
            dismissable=True,
            is_open=True,
        ),
    ])


header = dbc.Card(
    dbc.CardBody(
        html.H2("한글 → [hɑŋɡɯl]",
                style={'text-align': 'center',
                       'fontWeight': 'bold',
                       'height': '100px',
                       'line-height': '70px'})
    ),
    color='#002145',
    inverse=True,
    style={'height': '100px', 'marginTop': '10px', 'marginBottom': '20px'},

)


ipa_parameters = dbc.Checklist(
    options=[
        {"label": "Palatalization 구개음화", "value": "p"},
        {"label": "Aspiration 격음화", "value": "a"},
        {"label": "Manner assimilation 음운동화", "value": "s"},
        {"label": "Post-obstruent tensification", "value": "t"},
        {"label": "Complex coda simplification 자음군단순화", "value": "c"},
        {"label": "Coda neutralization 음절말 장애음 중화", "value": "n"},
        {"label": "(Optional) intersonorant H-deletion", "value": "h"},
        {"label": "(Optional) non-coronalization", "value": "o"},
        {"label": "(Phonetic) intersonorant obstruent voicing", "value": "v"},
        {"label": "(Phonetic) liquid alternation", "value": "r"},
        ],
    value=list('pastcnhovr'),
    id="parameter-checklist",
)


yale_parameters = dbc.Checklist(
    options=[
        {"label": "High vowel neutralization (i.e., High vowels must be unrounded after a bilabial)", "value": "u"},
        ],
    value=list('u'),
    id="parameter-checklist",
)


collapsed_parameter_setter = dbc.Collapse(
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
                inline=True,
                className="mb-4"
            ),
            dbc.Label("Phonological rules", style={'fontWeight': 'bold'}),
            dbc.Row(ipa_parameters, id='transcription_settings', className='mb-3'),
            dbc.Label("Segments are separated by...", style={'fontWeight': 'bold'}),
            dbc.Input(id="separator", value="", type="text", maxLength=1),
            dbc.FormText(id="sep-example", children="Preview: hɑŋɡɯl")
        ],
        body=True),
    id="settings",
    is_open=False,
)


output_card = dbc.Card(
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
    )
