# hangul_to_ipa
A dash app that transcribes 한글 into [hɑŋɡɯl].

**Enter 한글, get [hɑŋɡɯl].**
**Click [here](https://hangul-to-ipa.herokuapp.com/) to use.**

This web app applies phonological rules to Korean orthographic forms (Hangul/Hangeul/한글) and transcribes them into IPA. You can use this app to apply one or more phonological rules from [Shin, Kiaer, and Cha (2012) Ch. 8](https://doi.org/10.1017/CBO9781139342858.010). A similar database of Korean surface forms (i.e., the outputs of rule applications) is available as K-SPAN by [Holliday, Turnbull and Eychenne (2017)](https://link.springer.com/article/10.3758/s13428-016-0836-8), though they do not provide on-the-spot transcription nor selectively applying a subset of Korean phonological rules.

In addition to automatic transcription, this program:
 * transliterates Korean orthography in accordance with the Yale Romanization of Korean. The Yale convention is a de facto standard in Korean linguistics. See Martin, Samuel E. (1992). A Reference Grammar of Korean. for details.
 * transcribes Chinese characters as pronounced in Korean. For example, 不正確 'imprecise' is transcribed as [pudʑʌŋwak]

Notably, this program focuses on phonological rules: i.e., investigating the effects of each rule application and showing hypothetical forms with or without rule applications. Thus, it does not apply most of the rules that are sensitive to morphological or other extra-phonological information. Therefore, it works best with monomorphemic words and may not produce reliable outputs otherwise. For instance, Compensatory Vowel Lengthening, Vowel Deletion, Glide Formation, and others cannot be implemented without morphological information. Likewise, /n/-Insertion and /l/-Tensification need etymological information.

Its earlier R implementation was motivated by '[hangul converter](https://github.com/stannam/KPNN/blob/master/hangul_converter.r),' a part of [KPNN](https://github.com/stannam/KPNN). 

## How to use

 1. (see the image below) Enter your Korean word (e.g., 예시입니다 'this is an example', 韓國語 'the Korean language', or 음운론 'phonology') in the textbox marked red. The results will show up in the blue circle at the bottom.

 <img src= "https://github.com/stannam/hangul_to_ipa/assets/43150234/ef0be14b-d608-4b32-b38c-59882b7bfe7c" width=60% />
 
 2. Click the 'Advanced' button to open advanced settings.
   
 3. (see the image below) Select either 'IPA Transcription' or 'Yale Romanization.' 

 <img src= "https://github.com/stannam/hangul_to_ipa/assets/43150234/f8b57430-1f37-483d-b6b4-3de656351791" width=60% />

 4. (see the image below) Choose to apply all or some phonological rules. See below for phonological rules implemented in this program. NB: Yale Romanization transliterates the spelling, so phonological rules are irrelevant.

 <img src= "https://github.com/stannam/hangul_to_ipa/assets/43150234/79d65296-eb06-4232-a87d-e5361f57a54f" width=60% />

 5. You can also upload a text file and get it transcribed/transliterated. The file should be column-delimited. Here are example files [file1](https://blog.kakaocdn.net/dn/dIRnEk/btrIADmZAEY/F24hptgcGcmqeKFMFA2Yr0/가로예시.txt?attach=1&knm=tfile.txt) [file2](https://blog.kakaocdn.net/dn/bV4ktG/btrIBUa5fGe/tZnsSpYrUwPUGGv45ZkZAk/세로예시.txt?attach=1&knm=tfile.txt)

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
See [Shin, Kiaer, and Cha (2012) Ch. 8](https://doi.org/10.1017/CBO9781139342858.010) for details.

### Morphological
1. Palatalization 구개음화 (e.g., mɑt-i -> mɑdʒi 'the eldest child')

### Phonological
1. Aspiration 격음화 (e.g., pukhɑn -> pukʰɑn 'North Korea')
1. Place assimilation 음운동화 (e.g., Obstruent nasalisation, Liquid nasalisation and Lateralisation in Shin et al 2012)
1. Post-obstruent tensification 필수적 경음화 (e.g., pɑksu -> pɑks*u 'hand clap')
1. Complex coda simplification 자음군단순화 (e.g., talk-to -> takto 'Chicken-also' NB: the SR must be [takt*o])
1. Coda neutralization 음절말 장애음 중화 (e.g., bitɕʰ, bitɕ, bis -> bit 'light / debt / hair comb')

### Optional
1. (Optional) intersonorant H-deletion 공명음사이 'ㅎ' 삭제 (e.g., sʌnho → sʌno 'preference')
1. (Optional) non-coronalization 수의적 조음위치동화 (e.g., hɑnkɯl → hɑŋɡɯl 'the Korean alphabet')

### Phonetic
1. (Phonetic) intersonorant obstruent voicing 장애음 유성음화 (e.g., tɕikɑk → tɕiɡɑk 'being late')
1. (Phonetic) liquid alternation [l ~ ɾ] (e.g., tʰɑlɑk → tʰɑɾɑk 'depravity')
