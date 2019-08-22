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
df = lsan_survey() # initiate lsan_survey class
df.data = pd.read_csv('survey.csv', index_col='PIN') # load csv data file
df.score_hexaco() # score subscales in HEXACO Personality Inventory (60-item)
df.score_isel() # score subscales in the Interpersonal Support Evaluation List (40-item)
```
```
# join all scored data and store in new DataFrame
new_df = df.append_data()
```