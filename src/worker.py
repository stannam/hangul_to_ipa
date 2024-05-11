import regex as re
import csv
from hangul_tools import hangul_to_jamos, jamo_to_hangul

class ConversionTable(object):
    def __init__(self, name):
        self.name = name
        # Open the tab-delimited file located in the 'stable' folder
        with open(f'../stable/{self.name}.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',')
            # Iterate over each row in the file
            for row in reader:
                # For each header, set it as an attribute if it's not already set
                for header, value in row.items():
                    # Add the value to a list associated with the header
                    if not hasattr(self, header):
                        setattr(self, header, [])
                    getattr(self, header).append(value)
        # Convert lists to tuples because the contents should be immutable
        for header in reader.fieldnames:
            setattr(self, header, tuple(getattr(self, header)))


CT_double_codas = ConversionTable('double_coda')
CT_neutral = ConversionTable('neutralization')
CT_tensification = ConversionTable('tensification')
CT_assimilation = ConversionTable('assimilation')
CT_aspiration = ConversionTable('aspiration')


def transcription_convention(convention:str):
    # supported transcription conventions: ipa, yale, park
    return ConversionTable(convention)


def sanitize(word: str) -> str:
    """
    converts all hanja 漢字 letters to hangul
    """
    if len(word) < 1:  # if empty input, no sanitize
        return word

    hanja_idx = [match.start() for match in re.finditer(r'\p{Han}', word)]
    if len(hanja_idx) == 0:  # if no hanja, no sanitize
        return word

    from hanja_tools import hanja_cleaner  # import hanja_cleaner only when needed
    r = hanja_cleaner(word, hanja_idx)
    return r


def separate_double_coda(syllables: list[str]) -> list:
    r = []
    for syllable in syllables:
        if len(syllable) < 3:
            r.append(syllable)
            continue
        coda = syllable[2]
        try:
            separated_coda = CT_double_codas.separated[CT_double_codas.double.index(coda)]
            r.append(syllable[:2] + separated_coda)
            continue
        except ValueError:
            r.append(syllable)
            continue
    return r


def remove_empty_onset(syllables: list[str]) -> list:
    r = []
    for syllable in syllables:
        to_append = syllable[1:] if syllable[0] == 'ㅇ' else syllable
        r.append(to_append)
    return r


def to_jamo(hangul: str, no_empty_onset: bool = True, sboundary: bool = False) -> str:
    # Convert Hangul forms to jamo, remove empty onset ㅇ
    # e.g., input "안녕" output "ㅏㄴㄴㅕㅇ"
    jamo_forms = hangul_to_jamos(hangul)

    jamo_forms = separate_double_coda(jamo_forms)   # divide double coda (e.g., "ㄳ" -> "ㄱㅅ")

    if no_empty_onset:  # remove soundless syllable initial ㅇ
        jamo_forms = remove_empty_onset(jamo_forms)

    if sboundary:
        # not implemented
        pass

    return ''.join(jamo_forms)


if __name__ == "__main__":
    print(to_jamo("앉녕하세요"))
