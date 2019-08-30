# LSAN_tools

Python toolbox with general-purpose functions for behavioral and neuroimaging research

## Installation
```
pip install git+https://github.com/LabSocialAffectNeuro/lsan_tools
```

## Dependencies
- pandas>=0.24

## lsan_survey 
Python class used to score self-report surveys

**Current scales included:**
- HEXACO Personality Inventory (60-item)
- Relational Mobility Scale (12-item)
- Interpersonal Support Evaluation List (40-item)
- Domain-Specific Risk-Taking (DOSPERT) Scale (60-item) 


### Example usage
``` 
from lsan_tools.utils import lsan_survey
```
```
survey = lsan_survey('survey.csv', 'PIN') # load data into lsan_survey class
survey.score_hexaco() # score subscales in HEXACO Personality Inventory (60-item)
survey.score_isel() # score subscales in the Interpersonal Support Evaluation List (40-item)

survey.retain_items(['age','gender']) # retain reports about single question items such as age or gender
```
```
# join all scored data and store in new DataFrame, but don't save to csv
new_survey = survey.join_data("scored_survey_output",save=False)
```