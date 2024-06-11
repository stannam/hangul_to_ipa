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
        {"label": "Palatalization 구개음화 (e.g., 맏이 mɑt-i -> mɑdʒi 'the eldest child')", "value": "p"},
        {"label": "Aspiration 격음화 (e.g., 녹화 nokhwa -> nokʰwa 'record')", "value": "a"},
        {"label": "Manner assimilation 음운동화 (cf. Obstruent Nasalisation, Liquid Nasalisation and Lateralisation in Shin et al 2012)", "value": "s"},
        {"label": "Post-obstruent tensification 필수적 경음화 (e.g., 박수 pɑksu -> pɑks*u 'hand clap')", "value": "t"},
        {"label": "Complex coda simplification 자음군단순화 (e.g., 닭도 talk-to -> takto 'Chicken-also' NB: the SR must be [takt*o])", "value": "c"},
        {"label": "Coda neutralization 음절말 장애음 중화 (e.g., 빛빚빗 bitɕʰ, bitɕ, bis -> bit 'light / debt / hair comb')", "value": "n"},
        {"label": "(Optional) intersonorant H-deletion 공명음사이 'ㅎ' 삭제 (e.g., 선호 sʌnho → sʌno 'preference')", "value": "h"},
        {"label": "(Optional) non-coronalization 수의적 조음위치동화 (e.g., 한글 hɑnkɯl → hɑŋɡɯl 'the Korean alphabet')", "value": "o"},
        {"label": "(Phonetic) intersonorant obstruent voicing 장애음 유성음화 (e.g., 부부 pupu → pubu 'married couple')", "value": "v"},
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
                    dbc.Label(
                        id='echo-input',
                        children='',
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
