
"This script is the main file that creates a Dash app.
Usage: app.R
"

# 1. Load libraries
library(dash)
library(here)
library(jsonlite)
library(utf8)
suppressPackageStartupMessages(library(plotly))
suppressPackageStartupMessages(library(tidyverse))

## load workers
source(here::here("worker.R"))

## behind the scene
all_rules <- list(
  'ipa' = list(c("Palatalization 구개음화 (e.g., mɑt-i → mɑdʒi 'the eldest child')\n","p"),
               c("Aspiration 격음화 (e.g., pukhɑn → pukʰɑn 'North Korea')\n","a"),
               c("Complex coda simplification 자음군단순화 (e.g., talk → tak 'Chicken')\n","c"),
               c("Manner assimilation 음운동화 (i.e., Obstruent nasalisation, Liquid nasalisation and Lateralisation)\n","s"),
               c("Post-obstruent tensification (e.g., pɑksu → pɑks*u 'hand clap')\n","t"),
               c("Coda neutralization 음절말 장애음 중화 (e.g., bitɕʰ / bitɕ / bis → bit 'light / debt / hair comb')\n","n"),
               c("Intervocalic H-deletion 모음사이 'ㅎ' 삭제 (e.g., sʌnho → sʌno 'preference')\n","h"),
               c("Intervocalic obstruent voicing 장애음 유성음화 (e.g., tɕikɑk → tɕiɡɑk 'being late')\n","v"),
               c("Optional non-coronalization 수의적 조음위치동화 (e.g., hɑnkɯl → hɑŋɡɯl 'the Korean alphabet')\n","o")
               ),
  'yale' = list(c('High vowel neutralization (i.e., High vowels must be unrounded after a bilabial)','u'))
)

sample_pool <- c("안녕하세요", "너는 음운론이 좋니?",  # random sentences
                 "닭도리탕", "읊지마", "밝잖니",   # complex coda simplification
                 "각막", "법률", "범람", # nasalization
                 "한라산", "발냄새", # lateralization
                 "밥물", "햇님", "억만장자", # manner assimilation
                 "굳이?", "맏이",  # palatalization
                 "툭하면",  # aspiration
                 "박수", # Post-obstruent tensification
                 "만화", # optional h-deletion
                 "한글", "감기", "신문" # optional non-coronalization
                 )  
sample_word <- sample(sample_pool,1)# the first word that is randomly presented to the user

## Assign components to variables
heading_title <- dash::h1('한글 → [hɑŋɡɯl]')

## Specify layout elements
div_header <- dash::div(
  list(
    heading_title
  ),
  style = list(
    backgroundColor = '#282b48', 
    textAlign = 'center',
    color = 'white',
    margin = 5,
    marginTop = 0
  )
)

div_side <- dash::div(
  list(
    dash::h2("Use this app to transcribe 한글 into [haŋgɯl]"),
    html$label("Enter your Korean word(s) below and get it transcribed in IPA or romanized in the Yale system."),
    dash::br(),
    dash::br(),
    
    # textbox interface
    dccInput(id = 'text_input',value = sample_word, type = 'text', debounce = TRUE),
    dash::br(),
    dash::br(),
    
    # fileIO interface (upload wordlist and download results)
    ## html$label("Or, upload a wordlist as a .txt file. Make sure to set parameters below before uploading a file!"),
    ## dccUpload(id='upload-file', 
    ##          children=dash::div(list('Drag and Drop or ', dash::a('Select File'))),
    ##          style=list('width'='80%',
    ##                     'height' = '60px',
    ##                     'lineHeight'='60px',
    ##                     'borderWidth'= '1px',
    ##                     'borderStyle'= 'dashed',
    ##                     'borderRadius'= '5px',
    ##                     'textAlign'= 'center',
    ##                     'margin'= '10px'),
    ##          multiple=TRUE # does not allow uploading multiple files
    ##          ),
    ## dash::br(),
    ## dash::br(),
    dash::p("You can choose to apply all or some phonological rules.
        Click the link below for details"),
    dash::a('[Readme]', href='https://github.com/stannam/hangul_to_ipa#readme',target='_blank'),
    dash::br(),
    html$hr(),
    dash::h3("What do you want to do?"),
    dccRadioItems(
      id = 'conventions-radio',
      options = list(list(label = 'IPA Transcription\n', value = 'ipa'),
                     list(label = 'Yale Romanization', value = 'yale')),
      value = 'ipa'
    ),
    dash::br(),
    html$hr(),
    dash::h3("Phonological rules"),
    dccChecklist(id = 'rules-checkbox'),
    dash::br(),
    dash::a('[Help]',href='https://github.com/stannam/hangul_to_ipa/blob/main/README.md#phonological-rules-applied-in-this-order',target='_blank'),
    dash::br(),
    dash::br()
    
    
  ), style = list('background-color'='lightgrey', 
                  'columnCount'=1, 
                  'white-space'='pre-line',
                  'width'= '50%')
)

div_res <- dash::div(
  list(
    div(id = 'input'),
    div(id = 'output'),
    dash::br(),
    dash::br(),
    dash::br(),
    dash::br(),
    div(id='output-df')
  ), style = list('margin-left' = '10px'))

# 2. Create Dash instance
app <- Dash$new()

# 3. Specify App layout
app$layout(
  
  dash::div(
    list(
      # title bar
      div_header,
      
      # under the title bar -- contain side bar (description and data source), and main bar (two tabs)
      dash::div(
        list(
          # Side bar
          div_side,
          # main bar -- the two tabs
          div_res
        ), style=list('display'='flex',
                      'font-family'='Arial, Helvetica, sans-serif')
      )
    )
  )
)

## App Callbacks

# Select convention then different rules checklist show up
app$callback(
  output('rules-checkbox', 'options'),
  params = list(input('conventions-radio', 'value')),
  function(selected_convention) {
    rules_selected <- all_rules[[selected_convention]]
    lapply(rules_selected,
           function(r){
             list('label' = r[1],
                  'value' = r[2])
           })
  }
)

# Rule checklist should be default to all selected
app$callback(
  output('rules-checkbox', 'value'),
  params = list(input('conventions-radio', 'value')),
  function(selected_convention) {
    rules_selected <- all_rules[[selected_convention]]
    lapply(rules_selected,
           function(r){
             r[2]
           })
  }
)

# Print Input
app$callback(
  output('input','children'),
  params = list(input('text_input','value')),
  function(hangul_text){
    sprintf("your input: \"%s\"", hangul_text)
  }
)


# Print Output
app$callback(
  output('output','children'),
  params = list(
    input('text_input','value'),
    input('rules-checkbox','value'),
    input('conventions-radio', 'value')
    ),
  function(hangul_text, rule_selection, convention){
    if(length(hangul_text)==0){
      sprintf("  %s output: ", convention)
    } else {
    rules_chr = paste(unlist(rule_selection),collapse='')
    res = applyRulesToHangul(data = hangul_text, 
                             rules = rules_chr, 
                             convention = convention)
    sprintf("    %s output: [%s]", convention, res)
    }
    
  }
)


# File IO: If .txt uploaded, run the worker and throw a text file back.
## app$callback(
##   output('output-df', 'children'),
##   param = list(input('upload-file','contents'),
##                input('rules-checkbox','value'),
##                input('conventions-radio', 'value')),
##   function(inputfile, rule_selection, convention){
##     if(!is.null(unlist(inputfile))){
##       content_string = base64_dec(strsplit(unlist(inputfile),split=',')[[1]][2])
##       decoded = rawToChar(content_string)
##       df = read.csv(text=decoded, header=FALSE)
##       if(nrow(df) < ncol(df)){
##         df <- t(df)
##       }
##       for(coln in 1:ncol(df)){
##         determin = df[1,coln]
##         if(is.na(as.numeric(determin))){
##           process_this = df %>% select(coln)
##           colnames(process_this) <- "entry"
##           process_this <- head(process_this,100)
##           break
##         }
##       }
##       rules_chr = paste(unlist(rule_selection),collapse='')
##       res = applyRulesToHangul(data = process_this,
##                                rules = rules_chr,
##                                convention = convention)
##       browser()
##       
##       return(
##         res
##       )
##     }
##     
##     
##   }
## )

# 4. Run app, change for deploy online
## app$run_server(host = '0.0.0.0', port = Sys.getenv('PORT', 8050))

app$run_server(debug = T)  ## local debugging
