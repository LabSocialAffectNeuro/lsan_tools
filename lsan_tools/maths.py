import pandas as pandas
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

def shuffle(df):
    """
    Take a DataFrame where the columns are variables and the 
    observations are the rows (e.g., row indices are subject IDs),
    and randomly shuffles the row indices.
    """
    
    new_df = df.copy()
    new_df['new_id'] = np.random.permutation(new_df.index)

    # get rid of added column
    new_df.index = (new_df['new_id'])
    
    # get rid of index name
    new_df.index.name = None

    # Now have subjects x variables DataFrame with subject IDs randomly shuffled.
    return new_df


def standardize(df, var_list):
	""" 
	Takes DateFrame and z-scores values within each of the columns
	"""
	scaler = StandardScaler()
	return scaler.fit_transform(df[var_list])

