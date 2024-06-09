import regex as re
from classes import ConversionTable, Word
import rules


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

    from hanja_tools import hanja_cleaner  # import hanja_cleaner only when needed
    r = hanja_cleaner(word, hanja_idx)
    return r


def convert(hangul: str, rules_to_apply: str = 'pastcnhovr', convention: str = 'ipa'):
    # the main function for IPA conversion

    if len(hangul) < 1:  # if no content, then return no content
        return ""

    # prepare
    rules_to_apply = rules_to_apply.lower()
    CT_convention = transcription_convention(convention)
    hangul = sanitize(hangul)
    word = Word(hangul=hangul)

    # resolve word-final consonant clusters right off the bat
    rules.simplify_coda(word, word_final=True)

    # apply rules
    word = rules.apply_rules(word, rules_to_apply)

    # high mid/back vowel merger after bilabial (only for the Yale convention)
    if CT_convention.name == 'yale':
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

    return transcribed


if __name__ == "__main__":
    pass
