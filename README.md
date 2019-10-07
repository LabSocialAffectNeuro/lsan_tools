# LSAN_tools

Python toolbox with general-purpose functions for behavioral and neuroimaging research

## Installation
```
pip install git+https://github.com/LabSocialAffectNeuro/lsan_tools
```

## Dependencies
- pandas>=0.24

## lsan_survey 
Python class used to perform manipulations on self-report surveys (e.g., score questionnaires, extract specific participants' data, etc.)

**Scoring functions:**
- HEXACO Personality Inventory (60-item): `lsan_survey.score_hexaco()`
- Relational Mobility Scale (12-item): `lsan_survey.score_rel_mobility()`
- Interpersonal Support Evaluation List (40-item): `lsan_survey.score_isel()`
- Domain-Specific Risk-Taking (DOSPERT) Scale (60-item): `lsan_survey.score_dospert()`

**Other functions:**
- Select specific subject data from survey using sub_ids.txt file, rewrite survey.data in class, but do not save as comma-separated file: `lsan_survey.select_data("sub_ids.txt", rewrite_to_self=True)`
- Retain specific question items (e.g., demographics): `lsan_survey.retain_items(list)`
- Join scored surveys and save as comma-delimited file: `lsan_survey.join_data()`

### Example usage
``` 
from lsan_tools.utils import lsan_survey
```
```
survey = lsan_survey('survey.csv', 'PIN') # load data into lsan_survey class
survey.select_data([101,102], rewrite_to_self=True, save=False) # only select subject IDs 101 and 102 from original data

survey.score_hexaco() # score subscales in HEXACO Personality Inventory (60-item)
survey.score_isel() # score subscales in the Interpersonal Support Evaluation List (40-item)

survey.retain_items(['age','gender']) # retain reports about single question items such as age or gender
```
```
# join all scored data and store in new DataFrame called new_survey and save to .csv called "scored_survey_output.csv"
survey.join_data(filename="scored_survey_output")
```