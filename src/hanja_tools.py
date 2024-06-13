import csv
from src.hangul_tools import hangul_to_jamos, jamo_to_hangul
from pathlib import Path

HIGHV_DIPHTHONGS = ("ㅑ", "ㅕ", "ㅖ", "ㅛ", "ㅠ", "ㅣ")


def realize_hanja(raw: str) -> str:
    # convert the Unicode code point (e.g., U+349A) into actual hanja 㒚
    stripped_raw = raw.strip('U+')  # 'U+' part is meaningless so strip
    r = chr(int(stripped_raw, 16))  # hexadecimal part into int and then into character
    return r


def load_jajeon() -> dict:
    # import a 漢字 - 한글 conversion table
    jajeon = {}
    jajeon_path = Path(__file__).parent.parent / 'tables' / 'hanja.tsv'
    with open(jajeon_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            # the original file uses the Unicode code point (e.g., U+349A), so need to convert this to the actual hanja
            key = realize_hanja(row[0])
            value = row[1]
            jajeon[key] = value
    return jajeon


def hanja_to_hangul(jajeon: dict, char:str) -> str:
    try:
        r = jajeon[char]
    except KeyError:
        r = char
    return r


def initial_rule(char: str) -> str:
    # apply the 'initial rule' (두음규칙) where 'l' becomes 'n' and 'n' gets deleted word-initially
    # char: hangul character
    changed_flag = False
    jamos = hangul_to_jamos(char)
    jamos = ''.join(jamos)
    onset, nucleus = jamos[0], jamos[1]
    if onset == 'ㄹ':
        onset = 'ㄴ'
        changed_flag = True
    if onset == 'ㄴ' and nucleus in HIGHV_DIPHTHONGS:
        onset = 'ㅇ'
        changed_flag = True

    if changed_flag:
        jamo_list = list(jamos)
        jamo_list[0], jamo_list[1] = onset, nucleus
        jamos = ''.join(jamo_list)

    return jamo_to_hangul(jamos)


def hanja_cleaner(word: str, hanja_loc:list[int]) -> str:
    jajeon = load_jajeon()
    chars = list(word)

    for i in hanja_loc:
        if chars[i] in ["不", "不"] and (i < len(chars) - 1):  # if 不 appears in a non-ultimate syllable
            if chars[i + 1] == "實":
                # special case: 不實 = 부실
                chars[i] = "부"
                chars[i + 1] = "실"
                continue
            else:
                # special case: 不 is pronounced as 부[pu] before an alveolar ㄷㅈ
                chars[i + 1] = hanja_to_hangul(jajeon, chars[i + 1])
                next_syllable = hangul_to_jamos(chars[i + 1])
                following_onset = ''.join(next_syllable)[0]
                chars[i] = "부" if following_onset in ["ㄷ", "ㅈ"] else "불"
                continue

        chars[i] = hanja_to_hangul(jajeon, chars[i])

        if i == 0:  # apply the 'initial rule' (두음법칙)
            chars[i] = initial_rule(chars[i])

    return ''.join(chars)


if __name__ == '__main__':
    pass