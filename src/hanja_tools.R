eval(parse(file=here::here("src","hangul_tools.R"), encoding="UTF-8"))
highV_diphthongs <- c("ㅑ","ㅕ","ㅖ","ㅛ","ㅠ","ㅣ")

# import a 漢字 - 한글 conversion table
jajeon <- jajeon <- read.csv(file=here::here("stable","hanja.tsv"), 
                             header=FALSE,
                             sep="\t")

intToHan <- function(han_int){
  split_han <- unlist(strsplit(han_int,split=""))
  length_han <- length(split_han)
  sep_loc <- grep("\\+",split_han)
  han_int <- tolower(paste0(split_han[(sep_loc+1):length_han],collapse=""))
  han_int <- paste0("0x",han_int,collapse="")
  return(intToUtf8(han_int))
}

# translate unicode items into human-readable characters
jajeon$V1 <- sapply(jajeon$V1, intToHan) 

# input a hanja character; return the corresponding hangul value
hanja_to_hangul <- function(syllable){
  res <- jajeon$V2[grep(syllable, jajeon$V1)]
  if(length(res) > 0) {
    return(res)
  }
  return(syllable)
}

# input a hanja-containing word; get a word free of hanja
hanja_cleaner <- function(syllables, hanja_loc){
  if(length(syllables) > 1){
    for(l in length(syllables):2){
      if(hanja_loc[l]){
        if(syllables[l]=="實" && (syllables[l-1]=="不"||syllables[l-1]=="不")){
          syllables[l-1] <- "부"
          hanja_loc[l-1] <- FALSE
          syllables[l] <- "실"
          hanja_loc[l] <- FALSE
        } else{
          syllables[l] <- hanja_to_hangul(syllables[l])
          new_onset <- unlist(strsplit(convertHangulStringToJamos(syllables[l]),split=""))[1]
          if(new_onset %in% c("ㄷ","ㅈ") && (syllables[l-1]=="不"||syllables[l-1]=="不")){
            syllables[l-1] <- "부"
            hanja_loc[l-1] <- FALSE
          }
        }
      }
    }
  }
  if(hanja_loc[1]){  # 한자가 어두인 경우.
    syllables[1] <- hanja_to_hangul(syllables[1])
    first_syllable <- unlist(strsplit(convertHangulStringToJamos(syllables[1]),split=""))
    if (first_syllable[1] == "ㄹ"){first_syllable[1] <- "ㄴ"}
    if (first_syllable[1] == "ㄴ" && first_syllable[2] %in% highV_diphthongs){
      first_syllable[1] <- "ㅇ"
    }
    syllables[1] <- assembleJamo(first_syllable)
    }
  return(paste0(syllables,collapse=""))

  
  
  
}