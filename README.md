# LSAN_tools

Python toolbox with general-purpose functions for behavioral and neuroimaging research

## Installation
```
pip install git+https://github.com/LabSocialAffectNeuro/lsan_tools
```

## Dependencies
- bids==0.9.5
- pandas>=0.24
- glob
- nipype==1.2.3
- numpy>=1.16.4
- os
- sklearn==0.21.2

## lsan_tools.behav.survey
Python class used to perform manipulations on self-report surveys (e.g., score questionnaires, extract specific participants' data, etc.)

**Scoring functions:**
- `survey.score_hexaco()`: Scores HEXACO Personality Inventory (60-item)
- `survey.score_rel_mobility()`: Scores Relational Mobility Scale (12-item)
- `survey.score_isel()`: Scores Interpersonal Support Evaluation List (40-item)
- `survey.score_dospert()`: Scores Domain-Specific Risk-Taking (DOSPERT) Scale (60-item) 

**Other functions:**
- `lsan_survey.select_data("sub_ids.txt", rewrite_to_self=True)`: Selects specific subject data from survey using sub_ids.txt file, rewrites survey.data in class, but does not save as comma-separated file
- `survey.retain_items(list)`: Retains specific question items (e.g., demographics)
- `survey.join_data()`: Joins scored surveys and save as comma-delimited file

### Example usage
``` 
from lsan_tools.behav import survey
```
```
survey = survey('survey.csv', 'PIN') # load data into lsan_survey class
survey.select_data([101,102], rewrite_to_self=True, save=False) # only select subject IDs 101 and 102 from original data

survey.score_hexaco() # score subscales in HEXACO Personality Inventory (60-item)
survey.score_isel() # score subscales in the Interpersonal Support Evaluation List (40-item)

survey.retain_items(['age','gender']) # retain reports about single question items such as age or gender
```
```
# join all scored data and store in new DataFrame called new_survey and save to .csv called "scored_survey_output.csv"
survey.join_data(filename="scored_survey_output")
```

## lsan_tools.fmri.postprep.events_class
(*in development*)
Python class used to take BIDS-formatted events.tsv files in a base BIDS directory and convert them for first-level GLM analysis in AFNI and SPM (FSL pending).

**Functions:**
- `events_class.get_timing()`: Throws timing information for each subject into dictionary and writes to BIDS derivatives folder for first-level GLM analysis in AFNI or SPM (Default: AFNI)
- `events.bunch_timing()`: Throws timing information for each subject into dictionary for first-level GLM analysis in nipype (*in-development*)

### Example usage
``` 
from lsan_tools.fmri.postprep import events_class
```
```
base_dir = '/mnt/data/bids_dir'
task_id = 'task_name_specified_in_bids'
events = events_class(base_dir, task_id)

events.get_timing(trimTRby=10, software='AFNI', write=True) # gets all trial types under task_id, and writes text files for AFNI analysis to BIDS derivatives folder

```
## lsan_tools.math
Some helpful math functions:
- `shuffle(df, type="pandas")`: Takes a pandas DataFrame where the columns are variables and the observations are the rows (e.g., subject IDs), and randomly shuffles the row indices
- `pairwise_vector(vec1, vec2, method="correlation", shuffle=False)`: Takes a pandas DataFrame and computes pairwise distance between two column vectors
- `standardize(df, var_list)`: Takes pandas DataFrame and z-scores values within each of the columns

## lsan_tools.utils
Some helpful data manipulation functions:
- `add_file_prefix(files_dir, prefix)`: Adds prefix to every file in a specified directory (wildcards in `files_dir` string work)