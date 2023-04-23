library(pbapply)
library(tidyverse)

# global variables
read_csv_resource <- function(file_name){
return (read_csv(file=here::here('stable',file_name), show_col_types = FALSE))
}

criteria_DoubleCoda <- read_csv_resource('double_coda.csv')
roman_ipa <- read_csv_resource('ipa.csv')
roman_yale <- read_csv_resource('yale.csv')
criteria_DoubleCoda <- read_csv_resource('double_coda.csv')
neutral <- read_csv_resource('neutralization.csv')
criteria_Tensification <- read_csv_resource('tensification.csv')
criteria_Assimilation <- read_csv_resource('assimilation.csv')
criteria_Aspiration <- read_csv_resource('aspiration.csv')


# load hangul-unicode interface
eval(parse(file=here::here("src","hangul_tools.R"), encoding="UTF-8"))


sanitize <- function(word) {
  if(nchar(word) < 1){  # if empty input, no sanitize
    return(word)
  }
  
  syllables <- unlist(strsplit(word,split=""))
  while(syllables[1]==" "){syllables <- syllables[2:length(syllables)]}
  hanja_loc <- grepl("[\\p{Han}]", syllables, perl=T)
  if(any(hanja_loc)){
    eval(parse(file=here::here("src","hanja_tools.R"), encoding="UTF-8"))
    word <- hanja_cleaner(syllables, hanja_loc)
  } else{
    word <- paste(syllables,collapse="")
  }
  
  return(word)
}

toJamo <- function(data, removeEmptyOnset = TRUE, sboundary = FALSE) {
  # Hangul forms to Jamo
  syllable <- convertHangulStringToJamos(data)
  for (j in 1:length(syllable)) {
    DC <- match(substr(syllable[j],3,3), criteria_DoubleCoda$double)
    if (is.na(DC) == FALSE) {					#겹받침을 둘로 나눔 (eg. "ㄳ" -> "ㄱㅅ")
      pre_combined <- c(substr(syllable[j], 1, 2), criteria_DoubleCoda$separated[DC])
      syllable[j] <- paste(pre_combined,collapse='')
      rm(pre_combined)
    } 
    if (removeEmptyOnset == TRUE){
      phonemic <- unlist(strsplit(syllable[j], split=""))	# 'syllable'의 j번째 element를 각 자모단위로 분리해서 새로운 vector 'phonemic'에 넣습니다.
      if(phonemic[1] == "ㅇ") {phonemic[1] <- ""}		# 첫번째 자모(즉, 초성)가 'ㅇ'이면, 그것을 제거합니다.
      syllable[j] <- paste(phonemic, collapse="")		# 'phonemic'을 결합해서 다시 음절단위로 만듭니다. 그러나 초성의 ㅇ은 제거된 상태입니다.
    }
    
  }
  
  if (sboundary == TRUE){
    syllable <- paste0(syllable,"$")
    syllable[length(syllable)] <- substr(syllable[length(syllable)],1,nchar(syllable[length(syllable)])-1)
  }
  
  jamo <- paste(syllable, collapse="")				# 그 결과를 jamo에 저장합니다.
  return(jamo)
}

CV_mark <- function(input){
  # This function is for identifying a Jamo as either consonant or vowel.
  output <- vector()
  phoneme <- unlist(strsplit(input,split=""))
  for (j in 1:length(phoneme)){
    if (is.na (match (phoneme[j], roman_ipa$C)) == TRUE) {
      phoneme[j]="V"
    }
    else {phoneme[j]="C"
    }
  }
  output <- paste(phoneme, collapse="")
  return(output)
}

applyRulesToHangul <- function(data, 
                               entry = "entry", 
                               rules = "pacstnhv",
                               convention = "ipa"){
  # 규칙의 종류와 순서
  # (P)alatalization: 구개음화 (맏이 -> 마지)
  # (A)spiration: 격음화 (북한 -> 부칸)
  # (C)omplex coda simplification: 자음군단순화 (닭도 -> 닥도, 닭 -> 닥)
  # a(S)similation: 음운동화
  # (T)ensification: 표준발음법 제23항(예외없는 경음화) 적용
  # coda (N)eutralization: 음절말 장애음 중화 (빛/빚/빗 -> 빝)
  # intervocalic (H)-deletion: 공명음 사이 'ㅎ' 삭제
  # intervocalic Obstruent (V)oicing: 공명음 사이 장애음 유성음화
  
  if (class(data)[1]!="character") {
    if (any(class(data)=="data.frame")){
      if (is.null(data[[entry]])){
        stop("Please specify a value for 'entry' parameter (a column name for wordforms). Default = 'entry'")
      }
      list.data <- as.list(data[[entry]])
      surface <- rapply(list.data, 
                        applyRulesToHangul, 
                        entry = entry, 
                        rules = rules,
                        convention = convention)
      surface <- as.vector(surface)
      data[["output"]] <- surface
      result <- data
      return(result)
    } else stop("Please input a character, data.frame or tbl object.")
  }
  
  if(nchar(data) < 1){  # if no content, then return no content
    return("")
  }
  print(data)
  rules <- tolower(rules)

  data <- sanitize(data)  # the function 'sanitize' converts all Hanja into hangul and removes string initial spaces
  jamo <- toJamo(data, removeEmptyOnset = T)
  if(grepl("p",rules) && (grepl("ㄷㅣ", jamo) || grepl("ㅌㅣ", jamo))){
    syllable <- convertHangulStringToJamos(data)
    for (j in 1:length(syllable)) {
      DC <- match(substr(syllable[j],3,3), criteria_DoubleCoda$double)
      if (is.na(DC) == FALSE) {					#겹받침을 둘로 나눔 (eg. "ㄳ" -> "ㄱㅅ")
        substr(syllable[j], 3, 4) <- as.character(criteria_DoubleCoda$separated[DC])
      } 
      phonemic <- unlist(strsplit(syllable[j], split=""))	# 'syllable'의 j번째 element를 각 자모단위로 분리해서 새로운 vector 'phonemic'에 넣습니다.
      if(!is.na(phonemic[3]) & phonemic[3] == "ㄷ") {phonemic[3] <- "x"}
      if(!is.na(phonemic[3]) & phonemic[3] == "ㅌ") {phonemic[3] <- "X"}
      if(phonemic[1] == "ㅇ") {phonemic[1] <- ""}		# 첫번째 자모(즉, 초성)가 'ㅇ'이면, 그것을 제거합니다.
      
      syllable[j] <- paste(phonemic, collapse="")		# 'phonemic'을 결합해서 다시 음절단위로 만듭니다. 그러나 초성의 ㅇ은 제거된 상태입니다.
    }
    
    jamo <- paste(syllable, collapse="")				# 그 결과를 jamo로.
    jamo <- gsub("xㅣ","ㅈㅣ",jamo)             # 구개음화 처리
    jamo <- gsub("Xㅣ","ㅊㅣ",jamo)
    jamo <- gsub("x","ㄷ",jamo)
    jamo <- gsub("X","ㅌ",jamo)
  }
  
  if(grepl("a",rules) && grepl("ㅎ",jamo)){
    for (l in 1:nrow(criteria_Aspiration)){
      if(grepl(criteria_Aspiration$from[l],jamo)){
        jamo <- sub(criteria_Aspiration$from[l], criteria_Aspiration$to[l], jamo)
      }
    }
  } 
  
  if(nchar(jamo) < 1){
    return("")
  }
  
  cv <- CV_mark(jamo)
  
  if(grepl("c",rules)){
    CCC_location<-unlist(gregexpr("VCCC",cv))
    if (any(CCC_location > 0)) {
    for (l in rev(CCC_location)){
      CCC_part<-substr(jamo,l+1,l+2)
      for (m in 1:nrow(criteria_DoubleCoda)){
        if(grepl(criteria_DoubleCoda$separated[m],CCC_part)){
          jamo <- paste(substr(jamo,1,l),criteria_DoubleCoda$to[m],substr(jamo,l+3,nchar(jamo)),sep="")
          cv <- paste(substr(cv,1,l),"C",substr(cv,l+3,nchar(cv)),sep="")
        }
      }
      rm(CCC_part)
    }
    }
    # 이상 CCC ->CC 해결
    # 아래 부분은 단어 끝에 나오는 자음연쇄(겹받침)의 음가를, 마치 뒤에 자음이 이어지는 것처럼 정해줌
    if(grepl("CC$",cv)){
      for (l in 1:nrow(criteria_DoubleCoda)){
        if(grepl(paste(criteria_DoubleCoda$separated[l],"$",sep=""),jamo)){
          jamo <- sub(criteria_DoubleCoda$separated[l],criteria_DoubleCoda$to[l],jamo)
          cv <- sub("CC$","C",cv)
        }
      }
    }
  }
  
  if(grepl("s",rules)){
    for (l in 1:nrow(criteria_Assimilation)){
      while(grepl(criteria_Assimilation$from[l],jamo)){
        jamo <- sub(criteria_Assimilation$from[l],criteria_Assimilation$to[l],jamo)
      }
    }
  }

  if(grepl("t",rules)){
    for (l in 1:nrow(criteria_Tensification)){
      while(grepl(criteria_Tensification$from[l],jamo)){
        jamo <- sub(criteria_Tensification$from[l],criteria_Tensification$to[l],jamo)
      }
    }
  }
  
  if(grepl("n",rules)){
    phoneme <- unlist(strsplit(jamo,split=""))
    for (l in 1:length(phoneme)){
      if(is.na(match(phoneme[l],neutral$from))==FALSE){
        if(l==length(phoneme)|unlist(strsplit(cv,split=""))[l+1]=="C"){
          phoneme[l] <- as.character(neutral$to[match(phoneme[l],neutral$from)])
          }
      }
      jamo <- paste(phoneme,collapse="")
    }
  }
  
  if(grepl("h",rules)){
    phoneme <- unlist(strsplit(jamo,split=""))
    split_cv <- unlist(strsplit(cv,""))
    h_location <- grep("ㅎ",phoneme[2:length(phoneme)])
    h_location <- h_location + 1
    h_deletion_criteria <- c("V","C","V")
    
    for (i in rev(h_location)){
      if (i < length(phoneme)){
        
        # check if /ㅎ/ comes after a sonorant
        if(grepl(phoneme[i-1], 'ㄴㄹㅇㅁ', fixed = TRUE)){ 
          split_cv <- c(split_cv[1:(i-1)], split_cv[(i+1):length(split_cv)])
          phoneme <- c(phoneme[1:(i-1)], phoneme[(i+1):length(phoneme)])
        } else {
          # check if /ㅎ/ comes in between two vowels
          check_h_deletion <- split_cv[(i-1):(i+1)]
          if (all(check_h_deletion == h_deletion_criteria)) {
            split_cv <- c(split_cv[1:(i-1)], split_cv[(i+1):length(split_cv)])
            phoneme <- c(phoneme[1:(i-1)], phoneme[(i+1):length(phoneme)])
          }  
        }
        
      }
    }
    
    cv <- paste0(split_cv, collapse="")
    jamo <- paste0(phoneme, collapse="")
    
    rm(phoneme, split_cv, h_location, h_deletion_criteria)
  }
  
  # 규칙적용 완료. 이하, IPA나 Yale로 변환.
  if (convention == "ipa"){
    romanization <- roman_ipa
  } else if (convention == "yale"){
    romanization <- roman_yale
  }
  jamo <- unlist(strsplit(jamo,split=""))
  for (l in 1:length(jamo)){
    if(is.na(match(jamo[l], romanization$C))==T){
      if(is.na(match(jamo[l], romanization$V))==T){
        if(jamo[l]!=' '){jamo[l]<-""}
      } else {
        jamo[l] <- as.character(romanization$VKlattese[match(jamo[l], romanization$V)])
      }
    } else {
      jamo[l]<-as.character(romanization$CKlattese[match(jamo[l],romanization$C)])}
  }
  
  # Yale convention에서 bilabial 뒤 high mid/back vowel merger 적용하기
  if (grepl("u", rules) && convention == "yale"){
    bilabials = c("p","pp","ph", "m") # 양순음 bilabial: ㅂㅃㅍㅁ
    for(j in 1:length(jamo)){
      if (jamo[j] %in% bilabials){
        if (!is.na(jamo[j+1]) && jamo[j+1] == "wu"){
          jamo[j+1] <- "u"
        }
      }
    }
  }
  
  # 음성작용인 intervocalic voicing 적용
  if (grepl("v", rules) && convention == "ipa"){
    sonorants = c("n","l","ŋ","m")
    cv_split = unlist(strsplit(cv, split=''))
    for(j in 1:length(jamo)){

      if(jamo[j] %in% sonorants || cv_split[j] == "V"){
        if(!is.na(jamo[j+2]) && (jamo[j+2] %in% sonorants || cv_split[j+2] == "V")){
          if(jamo[j+1]=="p"){jamo[j+1] <- "b"}
          if(jamo[j+1]=="t"){jamo[j+1] <- "d"}
          if(jamo[j+1]=="k"){jamo[j+1] <- "ɡ"}
          if(jamo[j+1]=="tɕ"){jamo[j+1] <- "dʑ"}
        }
      }
    }
    rm(sonorants, cv_split)
  }
  
  # 음성작용인 liquid alternation 적용
  if (grepl("r", rules) && convention == "ipa" && 'l' %in% jamo){
    cv_split = unlist(strsplit(cv, split=''))
    liquid_location <- grep("l",jamo)
    liquid_location <- liquid_location[liquid_location < length(jamo)]
    if (any(liquid_location > 0)) {
      for (l in liquid_location[liquid_location > 1]){
        if (cv_split[l-1] == "V" && cv_split[l+1] == "V"){
          jamo[l] <- "ɾ"
        }
      }
    }
    rm(cv_split, liquid_location)
  }
  
  # 수의작용인 non-coronalization 적용
  if (grepl("o", rules) && convention == "ipa"){
    velars = c("ɡ","k","k*","kʰ")
    bilabials = c("b","p","p*","pʰ","m")
    non_velar_nasals = c('m','n')
    for(j in 1:length(jamo)){
      
      if(jamo[j] %in% non_velar_nasals && !is.na(jamo[j+1])){
        if(jamo[j+1] %in% velars){
          jamo[j] <- "ŋ"
        } else if(jamo[j+1] %in% bilabials){
          jamo[j] <- "m"
        }
      }
    }
    rm(velars, bilabials, non_velar_nasals)
    
  }
  
  output <- paste(jamo, collapse="")

  return(output)
}
