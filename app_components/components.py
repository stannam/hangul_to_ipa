from dash import html, dcc
import dash_bootstrap_components as dbc
from app_components.sample_word import sample_word

donation_ribbon = dbc.Stack([
        dbc.Alert(
                ["If you're enjoying it, please consider ",
                 html.A("buying me a coffee.",
                        href="https://buymeacoffee.com/linguisting",
                        target="_blank",
                        className="alert-link"),
                 ],
                id="alert-fade",
                color="warning",
                dismissable=True,
                is_open=True,
                ),
        dbc.Alert(
            ["이 앱이 유익하다면 ",
             html.A("토스로 후원해주세요 (익명가능).",
                    href="https://toss.me/sleepywug",
                    target="_blank",
                    className="alert-link"),
             ],
            id="alert-fade-kor",
            color="warning",
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


input_box = dbc.Row(dbc.Col([
    dbc.Label(children="Enter your 한글:", id="hangul-input-label"),
    dbc.Input(id='hangul-input', placeholder=sample_word, type='text'),
    dbc.FormText("Type something in the box above. Upon launching, a random word will appear",
                 id='hangul-input-help',
                 className='mb-5'),
    ],
))


main_buttons = dbc.ButtonGroup(
    [
        dbc.Button(
            "Convert",
            id="convert-btn",
            className='mb-3',
            color='primary'
        ), dbc.Button(
            "우리말로",
            id='language-btn',
            className='mb-3',
            color='info',
            n_clicks=0
        ), dbc.Button(
            "Advanced",
            id='advanced-btn',
            className='mb-3',
            color='secondary',
            n_clicks=0
        ),
    ],
    className="me-1",
)


help_links = dbc.FormText(children=[
    html.A(children="어케함?", href="https://linguisting.tistory.com/67", target="_blank"),
    " | ",
    html.A(children="Help", href="https://github.com/stannam/hangul_to_ipa#readme", target="_blank"),
])


ipa_parameters = dbc.Checklist(
    options=[
        {"label": "Palatalization (e.g., mɑt-i -> mɑdʒi 'the eldest child')", "value": "p"},
        {"label": "Aspiration (e.g., nokhwa -> nokʰwa 'record')", "value": "a"},
        {"label": "Manner assimilation (cf. Obstruent Nasalisation, Liquid Nasalisation and Lateralisation in Shin et al 2012)", "value": "s"},
        {"label": "Post-obstruent tensification (e.g., pɑksu -> pɑks*u 'hand clap')", "value": "t"},
        {"label": "Complex coda simplification (e.g., talk-to -> takto 'Chicken-also' NB: the SR must be [takt*o])", "value": "c"},
        {"label": "Coda neutralization (e.g., bitɕʰ, bitɕ, bis -> bit 'light / debt / hair comb')", "value": "n"},
        {"label": "(Optional) intersonorant H-deletion (e.g., sʌnho → sʌno 'preference')", "value": "h"},
        {"label": "(Optional) non-coronalization (e.g., hɑnkɯl → hɑŋɡɯl 'the Korean alphabet')", "value": "o"},
        {"label": "(Phonetic) intersonorant obstruent voicing (e.g., pupu → pubu 'married couple')", "value": "v"},
        {"label": "(Phonetic) liquid alternation (e.g., 이리 ili → iɾi 'wolf')", "value": "r"},
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


ipa_parameters_ko = dbc.Checklist(
    options=[
        {"label": "구개음화 (예: mɑt-i -> mɑdʒi '맏이')", "value": "p"},
        {"label": "격음화 (예: nokhwa -> nokʰwa '녹화')", "value": "a"},
        {"label": "음운동화 (장애음 비음화, 유음 비음화, 유음화. Shin et al 2012)", "value": "s"},
        {"label": "장애음 뒤 경음화 (예: pɑksu -> pɑks*u '박수')", "value": "t"},
        {"label": "자음군단순화 (예: talk-to -> takto '닭도' 주의: 최종 표면형은 [takt*o])", "value": "c"},
        {"label": "음절말 평폐쇄음화 (예: bitɕʰ, bitɕ, bis -> bit '빛/빚/빗')", "value": "n"},
        {"label": "(선택) 공명음사이 'ㅎ' 삭제 (예: sʌnho → sʌno '선호')", "value": "h"},
        {"label": "(선택) 수의적 조음위치동화 (예: hɑnkɯl → hɑŋɡɯl '한글')", "value": "o"},
        {"label": "(음성) 장애음 유성음화 (예: pupu → pubu '부부')", "value": "v"},
        {"label": "(음성) 유음 변이음 선택 (예: ili → iɾi '이리')", "value": "r"},
        ],
    value=list('pastcnhovr'),
    id="parameter-checklist",
)


yale_parameters_ko = dbc.Checklist(
    options=[
        {"label": "양순음 뒤 고모음 중화", "value": "u"},
        ],
    value=list('u'),
    id="parameter-checklist",
)



file_io = dbc.Row(
    [dbc.Col(
        children=[
            dbc.Label("Convert a wordlist", style={'fontWeight': 'bold'}, id='convert-label'),
            dcc.Upload(id="upload-data",
                       children="Drag and drop or click here to upload a wordlist (.txt)",
                       style={
                           'width': '100%',
                           'height': '60px',
                           'lineHeight': '60px',
                           'borderWidth': '1px',
                           'borderStyle': 'dashed',
                           'borderRadius': '5px',
                           'textAlign': 'center',
                           'margin': '5px'
                       },
                       multiple=False),
            dbc.FormText(id="upload-explain",
                         children=["Convert many words with the settings above. ",
                                   html.A("Example file for reference",
                                          href="https://blog.kakaocdn.net/dn/bwC5Ic/btrIRHihLsS/X2sZK9vql4HSftGvMoK2Gk/%EA%B0%80%EB%A1%9C%EC%98%88%EC%8B%9C.txt?attach=1&knm=tfile.txt",
                                          target="_blank",
                                          className="alert-link")
                                   ]),
        ]
    ),
     dcc.Download(id="download-processed-data")]
)


set_separator = dbc.Row(
    dbc.Col(
        children=[
            dbc.Label("Segments are separated by...", style={'fontWeight': 'bold'}, id='sep-help'),
            dbc.Input(id="separator", value=" ", type="text", maxLength=1),
            dbc.FormText(id="sep-example", children="Preview: hɑŋɡɯl"),
        ]
    ),
    className='mb-3'
)

collapsed_parameter_setter = dbc.Collapse(
    dbc.Card(
        [
            dbc.Label("What do you want to do?", style={'fontWeight': 'bold'}, id='what-want'),
            dbc.RadioItems(
                options=[
                    {"label": "IPA Transcription", "value": "ipa"},
                    {"label": "Yale Romanization", "value": "yale"},
                ],
                value='ipa',
                id="ipa-yale",
                inline=True,
                className="mb-3"
            ),
            dbc.Label("Phonological rules", style={'fontWeight': 'bold'}, id='phon-rules'),
            dbc.Row(ipa_parameters, id='transcription_settings', className='mb-3'),
            set_separator,
            file_io

        ],
        body=True),
    id="advanced",
    is_open=False,
)


output_card = dbc.Card(
        [
            dbc.Row([
                    dbc.Label("Your input:", style={'fontWeight': 'bold'}, id='input-label'),
                    dbc.Label(
                        id='echo-input',
                        children='',
                    ),
                    ],
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
            ),
        ],
        body=True,
        id="output",
        className='mb-3'
    )

footer = html.Footer(
    dbc.Container(
        dbc.Row(
            dbc.Col([
                html.A(
                    html.I(className="fab fa-github fa-2x"),  # GitHub icon
                    href="https://github.com/stannam/hangul_to_ipa",
                    target="_blank",
                    style={'marginRight': '20px'}
                ),
                html.A(
                    html.I(className="fas fa-mug-hot fa-2x"),  # Coffee icon
                    href="https://buymeacoffee.com/linguisting",
                    target="_blank",
                    style={'marginRight': '20px'}
                ),
                html.A(
                    html.I(className="fas fa-thumbs-up fa-2x"),  # Donate icon
                    href="https://toss.me/sleepywug",
                    target="_blank"
                ),
                ],
                className="text-center"
            )
        ),
        className="mt-4"
    ),
    style={
        "position": "fixed",
        "left": "0",
        "bottom": "0",
        "width": "100%",
        "backgroundColor": "#f8f9fa",
        "padding": "10px"
    }
)
