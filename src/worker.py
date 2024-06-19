# the engine that does the hard lifting.
# convert() is the entry point for converting Korean orthography into transcription

import regex as re
from base64 import b64decode
from typing import Union

from src.classes import ConversionTable, Word
import src.rules as rules


def transcription_convention(convention: str):
    # supported transcription conventions: ipa, yale, park
    convention = convention.lower()
    if convention not in ['ipa', 'yale', 'park']:
        raise ValueError(f"Your input {convention} is not supported.")
    return ConversionTable(convention)


def sanitize(word: str) -> str:
    """
    converts all hanja 漢字 letters to hangul
    and also remove any space in the middle of the word
    """
    if len(word) < 1:  # if empty input, no sanitize
        return word

    word = word.replace(' ', '')

    hanja_idx = [match.start() for match in re.finditer(r'\p{Han}', word)]
    if len(hanja_idx) == 0:  # if no hanja, no sanitize
        return word

    from src.hanja_tools import hanja_cleaner  # import hanja_cleaner only when needed
    r = hanja_cleaner(word, hanja_idx)
    return r


def convert(hangul: str,
            rules_to_apply: str = 'pastcnhovr',
            convention: str = 'ipa',
            sep: str = '') -> str:
    # the main function for IPA conversion

    if len(hangul) < 1:  # if no content, then return no content
        return ""

    # prepare
    rules_to_apply = rules_to_apply.lower()
    CT_convention = transcription_convention(convention)
    hangul = sanitize(hangul)
    word = Word(hangul=hangul)

    # resolve word-final consonant clusters right off the bat
    rules.simplify_coda(word)

    # apply rules
    word = rules.apply_rules(word, rules_to_apply)

    # high mid/back vowel merger after bilabial (only for the Yale convention)
    if CT_convention.name == 'yale' and 'u' in rules_to_apply:
        bilabials = list("ㅂㅃㅍㅁ")
        applied = list(word.jamo)
        for i, jamo in enumerate(word.jamo[:-1]):
            if jamo in bilabials and word.jamo[i+1] == "ㅜ":
                applied[i+1] = "ㅡ"
        word.jamo = ''.join(applied)

    # convert to IPA or Yale
    transcribed = rules.transcribe(word.jamo, CT_convention)

    # apply phonetic rules
    if CT_convention.name == 'ipa':
        transcribed = rules.apply_phonetics(transcribed, rules_to_apply)

    return sep.join(transcribed)


def convert_many(long_content: str,
                 rules_to_apply: str = 'pastcnhovr',
                 convention: str = 'ipa',
                 sep: str = '') -> Union[int, str]:
    # decode uploaded file and create a wordlist to pass to convert()
    decoded = b64decode(long_content).decode('utf-8')
    decoded = decoded.replace('\r\n', '\n').replace('\r', '\n')  # normalize line endings
    decoded = decoded.replace('\n\n', '')  # remove empty line at the file end

    input_internal_sep = '\t' if '\t' in decoded else ','

    if '\n' in decoded:
        # a vertical wordlist uploaded
        input_lines = decoded.split('\n')
        wordlist = [l.split(input_internal_sep)[1].strip() for l in input_lines if len(l) > 0]
    else:
        # a horizontal wordlist uploaded
        wordlist = decoded.split(input_internal_sep)

    # iterate over wordlist and populate res
    res = ['Orthography\tIPA']
    for word in wordlist:
        converted_r = convert(hangul=word,
                              rules_to_apply=rules_to_apply,
                              convention=convention,
                              sep=sep)
        res.append(f'{word.strip()}\t{converted_r.strip()}')

    return '\n'.join(res)


if __name__ == "__main__":
    example = convert("예시")
    print(example)   # jɛ s i
