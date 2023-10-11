GA_CODE <- 44032 # The unicode representation of the Korean syllabic orthography starts with GA_CODE
G_CODE <- 12593 # The unicode representation of the Korean phonetic (jamo) orthography starts with G_CODE
ONSET <- 588
CODA <- 28

# ONSET LIST. 00 -- 18
ONSET_LIST <- c('ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

# VOWEL LIST. 00 -- 20
VOWEL_LIST <- c('ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                'ㅣ')

# CODA LIST. 00 -- 27 + 1 (1 for open syllable)
CODA_LIST <- c('', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
               'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')

convertHangulStringToJamos <- function(word){
  split_word <- unlist(strsplit(word, split=''))
  output <- list()
  
  for (letter in split_word){
    syllable <- ""
    if (!all(is.na(str_match(letter, "[가-힣]")))){  # run this only for a Korean character
      chr_code <- utf8ToInt(letter) # returns the integer representing an Unicode character
      chr_code <- chr_code - GA_CODE
      
      if (chr_code < 0){
        syllable <- paste0(letter)
      }
      
      onset <- floor(chr_code / ONSET)
      vowel <- floor((chr_code - (ONSET * onset)) / CODA)
      coda <- floor((chr_code - (ONSET * onset) - (CODA * vowel)))
      
      
      syllable <- paste0(ONSET_LIST[onset+1], VOWEL_LIST[vowel+1], CODA_LIST[coda+1])
      
    } else {
      syllable <- paste0(letter)
      
    }
    output <- append(output, syllable)
  }
  
  output <- unlist(output)
  return(output)
}

assembleJamo <- function(syllable){
  # only accepts one syllable!
  if(length(syllable) > 1){
    onset <- grep(syllable[1],ONSET_LIST) - 1
    vowel <- grep(syllable[2],VOWEL_LIST) - 1
    coda <- 0
    if(length(syllable) == 3){
      coda <- grep(syllable[3],CODA_LIST) - 1
    }
    syllable <- intToUtf8((((onset * 21) + vowel) * 28) + coda + GA_CODE)
  }
  return(syllable)
}
