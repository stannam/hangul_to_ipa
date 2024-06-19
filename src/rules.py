# phonological rules
import regex as re

from src.classes import Word, ConversionTable
from typing import Union


CT_double_codas = ConversionTable('double_coda')
CT_neutral = ConversionTable('neutralization')
CT_tensification = ConversionTable('tensification')
CT_assimilation = ConversionTable('assimilation')
CT_aspiration = ConversionTable('aspiration')
CT_convention = ConversionTable('ipa')

CONSONANTS = tuple(list(CT_convention.C)[:-2])   # from the C column of the IPA table, remove special characters # and $
VOWELS = tuple(list(CT_convention.V))   # from the V column of the IPA table
C_SONORANTS = ('ㄴ', 'ㄹ', 'ㅇ', 'ㅁ')
OBSTRUENTS = tuple(set(CONSONANTS) - set(C_SONORANTS))
SONORANTS = VOWELS + C_SONORANTS


def get_substring_ind(string: str, pattern: str) -> list:
    return [match.start() for match in re.finditer(f'(?={pattern})', string)]


def transcribe(jamos: str, convention: ConversionTable = CT_convention, str_return: bool = False) -> Union[list, str]:
    transcribed = []
    for jamo in jamos:
        is_C = convention.safe_index('C', jamo)
        is_V = convention.safe_index('V', jamo)
        if is_V >= 0:
            transcribed.append(convention.VSymbol[is_V])
        elif is_C >= 0:
            transcribed.append(convention.CSymbol[is_C])

    if str_return:
        return ''.join(transcribed)
    return transcribed


def palatalize(word: Word) -> str:
    palatalization_table = {
        'ㄷ': 'ㅈ',
        'ㅌ': 'ㅊ'
    }
    hangul_syllables = list(word.hangul)
    to_jamo_bound = word.to_jamo
    syllables_in_jamo = [to_jamo_bound(syl) for syl in hangul_syllables]
    for i, syllable in enumerate(syllables_in_jamo):
        try:
            next_syllable = syllables_in_jamo[i + 1]
            if next_syllable[0] == 'ㅣ':
                new_coda = palatalization_table.get(syllable[-1], syllable[-1])
                syllables_in_jamo[i] = ''.join(list(syllables_in_jamo[i])[:-1] + [new_coda])
        except IndexError:
            continue
    new_jamo = ''.join(syllables_in_jamo)
    return new_jamo


def aspirate(word: Word) -> str:
    return CT_aspiration.sub(word.jamo)


def assimilate(word: Word) -> str:
    return CT_assimilation.sub(word.jamo)


def pot(word: Word) -> str:
    return CT_tensification.sub(word.jamo)


def neutralize(word: Word) -> str:
    new_jamos = list(word.jamo)
    for i, jamo in enumerate(new_jamos):
        if i == len(new_jamos) - 1 or word.cv[i + 1] == 'C':
            new_jamos[i] = CT_neutral.apply(jamo)
    return ''.join(new_jamos)


def delete_h(word: Word) -> str:
    h_locations = get_substring_ind(string=word.jamo, pattern='ㅎ')

    for h_location in reversed(h_locations):
        if h_location == 0 or h_location == len(word.jamo) - 1:
            # a word-initial h cannot undergo deletion
            continue
        preceding = word.jamo[h_location - 1]
        succeeding = word.jamo[h_location + 1]
        if preceding in SONORANTS and succeeding in SONORANTS:
            word.jamo = word.jamo[:h_location] + word.jamo[h_location + 1:]
    return word.jamo


def simplify_coda(input_word: Word, word_final: bool = False) -> Word:
    def simplify(jamo: str, loc: int) -> str:
        # coda cluster simplification

        list_jamo = list(jamo)
        before = ''.join(list_jamo[:loc + 1])
        double_coda = ''.join(list_jamo[loc + 1:loc + 3])
        after = ''.join(list_jamo[loc + 3:])

        converted = CT_double_codas.apply(text=double_coda, find_in='_separated')
        return before + converted + after

    while True:
        double_coda_loc = get_substring_ind(input_word.cv, 'VCCC')  # get all CCC location
        if len(double_coda_loc) == 0:
            break  # if no, exit while-loop

        cc = double_coda_loc[0]  # work on the leftest CCC
        new_jamo = simplify(input_word.jamo, cc)
        input_word.jamo = new_jamo

    # additionally, simplify word-final consonant cluster
    final_CC = get_substring_ind(input_word.cv, 'CC$')
    if len(final_CC) > 0:
        cc = final_CC[0] - 1
        new_jamo = simplify(input_word.jamo, cc)
        input_word.jamo = new_jamo
    return input_word


def non_coronalize(input_word: Word) -> str:
    velars = list('ㄱㅋㄲ')
    bilabials = list('ㅂㅍㅃㅁ')
    non_velar_nasals = list('ㅁㄴ')

    res = list(input_word.jamo)
    for i, jamo in enumerate(input_word.jamo[:-1]):
        if i == 0 or jamo not in non_velar_nasals:
            continue
        succeeding = input_word.jamo[i+1]
        if succeeding in velars:
            res[i] = 'ㅇ'
        elif succeeding in bilabials:
            res[i] = 'ㅁ'
    return ''.join(res)


def inter_v(symbols: list) -> list:
    voicing_table = {
        'p': 'b',
        't': 'd',
        'k': 'ɡ',
        'tɕ': 'dʑ'
    }
    ipa_sonorants = [transcribe(s, str_return=True) for s in SONORANTS]

    res = list(symbols)

    for index, symbol in enumerate(symbols[:-1]):
        if index == 0 or symbol not in voicing_table.keys():
            continue
        preceding = symbols[index - 1]
        succeeding = symbols[index + 1]

        if preceding in ipa_sonorants:
            if succeeding in ipa_sonorants:
                res[index] = voicing_table.get(symbol, symbol)
            elif succeeding == 'ɕ':
                res[index] = voicing_table.get(symbol, symbol)
                res[index + 1] = 'ʑ'

    return res


def alternate_lr(symbols: list) -> list:
    ipa_vowels = [transcribe(v, str_return=True) for v in VOWELS]

    res = list(symbols)

    l_locs = [index for index, value in enumerate(symbols) if value == 'l']

    for l_loc in reversed(l_locs):
        if l_loc == 0 or l_loc == (len(symbols) - 1):
            continue

        preceding = symbols[l_loc - 1]
        succeeding = symbols[l_loc + 1]
        if preceding in ipa_vowels and succeeding in ipa_vowels:
            res[l_loc] = 'ɾ'

    return res


def apply_rules(word: Word, rules_to_apply: str = 'pastcnhovr') -> Word:
    # 규칙의 종류와 순서
    # (P)alatalization: 구개음화 (맏이 -> 마지)
    # (A)spiration: 격음화 (북한 -> 부칸)
    # a(S)similation: 음운동화
    # (T)ensification: 표준발음법 제23항(예외없는 경음화) 적용
    # (C)omplex coda simplification: 자음군단순화 (닭도 -> 닥도, 닭 -> 닥)
    # coda (N)eutralization: 음절말 장애음 중화 (빛/빚/빗 -> 빝)
    # intersonorant (H)-deletion: 공명음 사이 'ㅎ' 삭제
    # intersonorant Obstruent (V)oicing: 공명음 사이 장애음 유성음화

    # apply palatalization
    if 'p' in rules_to_apply and ('ㄷㅣ' in word.jamo or 'ㅌㅣ' in word.jamo):
        word.jamo = palatalize(word)

    # apply aspiration
    if 'a' in rules_to_apply and 'ㅎ' in word.jamo:
        word.jamo = aspirate(word)

    # apply place assimilation
    if 's' in rules_to_apply:
        word.jamo = assimilate(word)

    # apply post-obstruent tensification
    if 't' in rules_to_apply and any(jm in word.jamo for jm in OBSTRUENTS):
        word.jamo = pot(word)

    # apply complex coda simplification
    if 'c' in rules_to_apply:
        word = simplify_coda(word)

    # apply coda neutralization
    if 'n' in rules_to_apply:
        word.jamo = neutralize(word)

    # apply intersonorant H-deletion
    if 'h' in rules_to_apply and 'ㅎ' in word.jamo[1:-1]:
        word.jamo = delete_h(word)

    # apply (optional) non-coronalization
    if 'o' in rules_to_apply:
        word.jamo = non_coronalize(word)

    return word


def apply_phonetics(ipa_symbols: list, rules_to_apply: str) -> list:
    if 'v' in rules_to_apply:
        ipa_symbols = inter_v(ipa_symbols)
    if 'r' in rules_to_apply and 'l' in ipa_symbols:
        ipa_symbols = alternate_lr(ipa_symbols)
    return ipa_symbols


if __name__ == '__main__':
    pass
