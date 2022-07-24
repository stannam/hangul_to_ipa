# hangul_to_ipa
A dash app that transcribes 한글 into [hɑŋɡɯl].

Enter 한글, get [hɑŋɡɯl].

This web app applies phonological rules to Korean orthographic forms (Hangul/Hangeul/한글) and transcribe them into IPA. It automatically applies phonological rules from [Shin, Kiaer, and Cha (2012) Ch. 8](https://doi.org/10.1017/CBO9781139342858.010). These are rules related to surface phonotactics and syllable structure constraints. The R implementation is motivated by '[hangul converter](https://github.com/stannam/KPNN/blob/master/hangul_converter.r),' a part of KPNN. 

This program does not apply most rules that are sensitive to morphological or other extra-phonological information. For instance, Compensatory Vowel Lengthening, Vowel Deletion, Glide Formation, and others cannot be implemented without morphological information. Likewise, /n/-Insertion and /l/-Tensification need etymological information.

## Inventory
### Consonants
![image](https://user-images.githubusercontent.com/43150234/180628409-4431b9f5-9517-4b32-b02a-ae6e7da694e8.png)
|           |           | Bilabial | Alveolar | Alveo-Palatal | Velar      | Glottal |
|:---------:|:---------:|----------|----------|---------------|------------|---------|
| Plosive   | Lenis     | ㅂ /p/   | ㄷ /t/   |               | ㄱ /k/     |         |
|           | Aspirated | ㅍ /pʰ/  | ㅌ /tʰ/  |               | ㅋ /kʰ/    |         |
|           | Fortis    | ㅃ /p*/  | ㄸ /t*/  |               | ㄲ /k*/    |         |
| Fricative | Aspirated |          | ㅅ /s/   |               |            | ㅎ /h/  |
|           | Fortis    |          | ㅆ /s*/  |               |            |         |
| Affricate | Lenis     |          |          | ㅈ /tɕ/       |            |         |
|           | Aspirated |          |          | ㅊ /tɕʰ/      |            |         |
|           | Fortis    |          |          | ㅉ /tɕ*/      |            |         |
|   Nasal   |           | ㅁ /m/   | ㄴ /n/   |               | 받침ㅇ /ŋ/ |         |
|  Lateral  |           |          | ㄹ /l/   |               |            |         |

### Vowels
![image](https://user-images.githubusercontent.com/43150234/180628552-bf099293-b86d-4a7d-af3a-61ee38a9fb6b.png)

|      |   Front  |    Back   |         |
|------|:--------:|:---------:|:-------:|
|      |          | Unrounded | Rounded |
| High |   ㅣ /i/  |   ㅡ /ɯ/  |  ㅜ /u/ |
| Mid  | ㅐㅔ /ɛ/ |   ㅓ /ʌ/  |  ㅗ /o/ |
| Low  |          |   ㅏ /a/  |         |

### Diphthongs
![image](https://user-images.githubusercontent.com/43150234/180628572-4fca5bf8-5ae7-4a16-aa29-ead935b200cf.png)
| 한글 | IPA  | 한글       | IPA  |
|------|------|------------|------|
| ㅠ   | /ju/ | ㅟ         | /wi/ |
| ㅕ   | /jʌ/ | ㅝ         | /wʌ/ |
| ㅛ   | /jo/ | ㅚ   ㅞ ㅙ | /wɛ/ |
| ㅖㅒ | /jɛ/ | ㅘ         | /wa/ |
| ㅑ   | /ja/ | ㅢ         | /ɰi/ |

## Phonological rules (applied in this order)

### Morphological
1. Palatalization 구개음화 (e.g., mɑt-i -> mɑdʒi 'the eldest child')

### Phonological
1. Aspiration 격음화 (e.g., pukhɑn -> pukʰɑn 'North Korea')
1. Complex coda simplification 자음군단순화 (e.g., talk-to -> takto 'Chicken-also' NB: the SR must be [takt*o])
1. Place assimilation 음운동화 (e.g., Obstruent nasalisation, Liquid nasalisation and Lateralisation in Shin et al 2012)
1. Post-obstruent tensification (e.g., pɑksu -> pɑks*u 'hand clap')
1. Coda neutralization 음절말 장애음 중화 (e.g., bitɕʰ / bitɕ / bis -> bit 'light / debt / hair comb')

### Phonetic / optional
1. Intervocalic H-deletion 모음사이 'ㅎ' 삭제 (e.g., sʌnho -> sʌno 'preference')
1. Intervocalic obstruent voicing 장애음 유성음화 (e.g., tɕikɑk -> tɕiɡɑk 'being late')


