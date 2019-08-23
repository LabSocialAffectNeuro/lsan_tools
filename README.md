# LSAN_tools

Python toolbox with general-purpose functions for behavioral and neuroimaging research

## Dependencies
- pandas

## lsan_survey 
Python class used to score self-report surveys

### Example usage
``` 
from lsan_tools.lsan_survey import lsan_survey
```
```
survey = lsan_survey('survey.csv', 'PIN') # load data into lsan_survey class
survey.score_hexaco() # score subscales in HEXACO Personality Inventory (60-item)
survey.score_isel() # score subscales in the Interpersonal Support Evaluation List (40-item)
```
```
# join all scored data and store in new DataFrame, but don't save to csv
new_survey = survey.join_data(save=False)
```