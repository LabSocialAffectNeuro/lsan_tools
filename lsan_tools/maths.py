import pandas as pandas
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

def shuffle(df, type="pandas"):
    """
    Take a DataFrame where the columns are variables and the 
    observations are the rows (e.g., row indices are subject IDs),
    and randomly shuffles the row indices.
    """
    if type == "pandas":
	    perm_data = df.copy()
	    perm_data['new_id'] = np.random.permutation(perm_data.index)

	    # get rid of added column
	    perm_data.index = (perm_data['new_id'])
	    
	    # get rid of index name
	    perm_data.index.name = None
	    
	elif type == "numpy":
		perm_data = np.random.permutation(df)

    # Now have subjects x variables DataFrame with subject IDs randomly shuffled.
    return perm_data



def standardize(df, var_list):
	""" 
	Takes DateFrame and z-scores values within each of the columns
	"""
	scaler = StandardScaler()
	return scaler.fit_transform(df[var_list])

