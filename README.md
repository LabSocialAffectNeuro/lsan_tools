# LSAN_tools

Python toolbox with general-purpose functions for behavioral and neuroimaging research

## Dependencies
- pandas

## lsan_survey 
Python class used to score self-reported surveys

### Example usage
``` 
from lsan_tools.data import lsan_survey
```
```
df = lsan_survey()
df.data = pd.read_csv('survey.csv', index_col='PIN')
df.score_hexaco() # score all subscales in HEXACO Personality Inventory (60-item)
```