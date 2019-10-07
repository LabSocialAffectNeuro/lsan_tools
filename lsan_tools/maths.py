import pandas as pandas
import numpy as np

def shuffle(df):
    """
    Take a dataframe where the columns are variables and the 
    subjects are the rows (row indices = subject IDs),
    and randomly shuffles the row labels.
    """
    
    df2 = df.copy()
    df2['new_id'] = np.random.permutation(df2.index)

    # get rid of added column
    df2.index = (df2['new_id'])
    
    # get rid of index name
    df2.index.name = None

    # Now have subjects x variables DataFrame with subject IDs randomly shuffled.
    return df2