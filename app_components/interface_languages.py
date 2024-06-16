# dictionaries for supporting more than one language
from dash import html

components_config = {
    'enter_hangul': {'id': 'hangul-input-label', 'property': 'children'},
    'type_something': {'id': 'hangul-input-help', 'property': 'children'},
    'convert': {'id': 'convert-btn', 'property': 'children'},
    'lang_change': {'id': 'language-btn', 'property': 'children'},
    'advanced': {'id': 'advanced-btn', 'property': 'children'},
    'convert_many': {'id': 'convert-label', 'property': 'children'},
    'drag_and_drop': {'id': 'upload-data', 'property': 'children'},
    'convert_wordlist': {'id': 'upload-explain', 'property': 'children'},
    'seperator-help': {'id': 'sep-help', 'property': 'children'},
    'ipa_or_yale': {'id': 'what-want', 'property': 'children'},
    'phonological_rules': {'id': 'phon-rules', 'property': 'children'},
    'your_input': {'id': 'input-label', 'property': 'children'}
}

translations = {
    'en': {
        'enter_hangul': 'Enter your 한글:',
        'type_something': "Type something in the box above. Upon launching, a random word will appear",
        'convert': "Convert",
        'lang_change': "우리말로",
        'advanced': "Advanced",
        'convert_many': "Convert a wordlist",
        'drag_and_drop': "Drag and drop or click here to upload a wordlist (.txt)",
        'convert_wordlist': ["Convert many words with the settings above. ",
                             html.A("Example file for reference",
                                    href="https://blog.kakaocdn.net/dn/bwC5Ic/btrIRHihLsS/X2sZK9vql4HSftGvMoK2Gk/%EA%B0%80%EB%A1%9C%EC%98%88%EC%8B%9C.txt?attach=1&knm=tfile.txt",
                                    target="_blank",
                                    className="alert-link")
                             ],
        'seperator-help': "Segments are separated by...",
        'ipa_or_yale': "What do you want to do?",
        'phonological_rules': "Phonological rules",
        'your_input': "Your input:"
    },
    'ko': {
        'enter_hangul': '변환할 한글을 입력하세요:',
        'type_something': "위 상자에 입력하세요. 앱 시작 시에는 무작위 단어가 나옵니다.",
        'convert': "변환하기",
        'lang_change': "English",
        'advanced': "고급",
        'convert_many': "단어목록 변환하기",
        'drag_and_drop': "단어목록 파일(.txt)을 여기로 끌어오거나 여기를 클릭하여 업로드하세요",
        'convert_wordlist': ["위 설정에 따라 많은 단어를 변환합니다. ",
                             html.A("처리 가능 파일 예시",
                                    href="https://blog.kakaocdn.net/dn/bwC5Ic/btrIRHihLsS/X2sZK9vql4HSftGvMoK2Gk/%EA%B0%80%EB%A1%9C%EC%98%88%EC%8B%9C.txt?attach=1&knm=tfile.txt",
                                    target="_blank",
                                    className="alert-link")
                             ],
        'seperator-help': "분절음 사이의 구분자...",
        'ipa_or_yale': "무엇을 할까요?",
        'phonological_rules': "음운규칙 목록",
        'your_input': "입력값:"

    }
}