
"This script is the main file that creates a Dash app.
Usage: app.R
"

# 1. Load libraries
library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
suppressPackageStartupMessages(library(plotly))
suppressPackageStartupMessages(library(tidyverse))

## load workers
source(here::here("worker.R"))

## behind the scene
all_rules <- list(
  'ipa' = list(c("Palatalization 구개음화 (e.g., mɑt-i → mɑdʒi 'the eldest child')\n","p"),
               c("Aspiration 격음화 (e.g., pukhɑn → pukʰɑn 'North Korea')\n","a"),
               c("Complex coda simplification 자음군단순화 (e.g., talk → tak 'Chicken')\n","c"),
               c("Place assimilation 음운동화 (i.e., Obstruent nasalisation, Liquid nasalisation and Lateralisation\n","s"),
               c("Post-obstruent tensification (e.g., pɑksu → pɑks*u 'hand clap')\n","t"),
               c("Coda neutralization 음절말 장애음 중화 (e.g., bitɕʰ / bitɕ / bis → bit 'light / debt / hair comb')\n","n"),
               c("Intervocalic H-deletion 모음사이 'ㅎ' 삭제 (e.g., sʌnho → sʌno 'preference')\n","h"),
               c("Intervocalic obstruent voicing 장애음 유성음화 (e.g., tɕikɑk → tɕiɡɑk 'being late')\n","v")
               ),
  'yale' = list(c('High vowel neutralization (i.e., High vowels must be unrounded after a bilabial)','u'))
)

## Assign components to variables
heading_title <- htmlH1('한글 → [haŋgɯl]')

## Specify layout elements
div_header <- htmlDiv(
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

div_side <- htmlDiv(
  list(
    dccMarkdown("
    **Use this app to transcribe 한글 into [haŋgɯl] (the IPA transcription of '한글')**"),
    html$label("Enter your Korean word(s) below and get it transcribed in IPA or romanized in the Yale system."),
    htmlBr(),
    dccInput(id = 'text_input',value = '안녕하세요', type = 'text', debounce = TRUE),
    htmlBr(),
    htmlBr(),
    dccMarkdown("You can choose to apply all or some phonological rules.
        See [here](https://github.com/stannam/hangul_to_ipa#readme) for details"),
    htmlBr(),
    html$hr(),
    dccMarkdown("**What do you want to do?**"),
    dccRadioItems(
      id = 'conventions-radio',
      options = list(list(label = 'IPA Transcription', value = 'ipa'),
                     list(label = 'Yale Romanization', value = 'yale')),
      value = 'ipa'
    ),
    htmlBr(),
    html$hr(),
    dccMarkdown("**Phonological rules ([help](https://github.com/stannam/hangul_to_ipa/blob/main/README.md#phonological-rules-applied-in-this-order))**"),
    dccChecklist(id = 'rules-checkbox'),
    html$hr()
    
    
  ), style = list('background-color'='lightgrey', 
                  'columnCount'=1, 
                  'white-space'='pre-line',
                  'margin-left' = '10px',
                  'width'= '50%')
)

div_res <- htmlDiv(
  list(
    div(id = 'input'),
    div(id = 'output')
  ), style = list('margin-left' = '10px'))

# 2. Create Dash instance
app <- Dash$new()

# 3. Specify App layout
app$layout(
  
  htmlDiv(
    list(
      # title bar
      div_header,
      
      # under the title bar -- contain side bar (description and data source), and main bar (two tabs)
      htmlDiv(
        list(
          # Side bar
          div_side,
          # main bar -- the two tabs
          div_res
        ), style=list('display'='flex')
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

# 4. Run app, change for deploy online
# app$run_server(host = '127.0.0.1', port = Sys.getenv('PORT', 8050))

app$run_server(debug = F)
