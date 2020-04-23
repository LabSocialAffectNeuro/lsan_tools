import pandas as pandas
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

def normalize_btwn_0_1(list_obj):
	"""
	Takes a list and normalizes the values from 0 (smallest) to 1(largest)
	"""
	return (list_obj-min(list_obj))/(max(list_obj)-min(list_obj))

def get_pairwise(behav_vct,type="absolute-dist",norm=True):
    
    """
    Takes a vector of behavioral scores (one per subject) and returns 
    the vectorized upper triangle of a similarity matrix constructed using:
    	A) absolute distance
    	B) average, or 
    	C) one formulation of the "AnnaK" principle 
    		(i.e., high-high pairs are most alike, low-low pairs are most dissimilar, and high-low pairs show intermediate similarity).
    		(all high scorers are alike, all low scorers are low-scoring in their own way)
    """    
    # Get dims
    n_subs = len(behav_vct)
    
    # Initialize output
    mtx = np.zeros((n_subs,n_subs))
    
    if norm:
    	behav_vct = normalize_btwn_0_1(behav_vct)

    # Fill in matrix
    for i in range(n_subs):
        for j in range(n_subs):
            if type == 'low-alike':
                mtx[i,j] = max(behav_vct[i], behav_vct[j])
                
            elif type == 'high-alike':
                mtx[i,j] = (1 - min(behav_vct[i], behav_vct[j])) #/n_subs
                
            elif type == 'average':
                mtx[i,j] = (behav_vct[i]+behav_vct[j])/2
                
            elif type == 'absolute-dist':
                mtx[i,j] = np.absolute(behav_vct[i]-behav_vct[j])
                
    # Compute upper triangle            
    vct = mtx[np.triu_indices(mtx.shape[0], k=1)]
    
    return vct, mtx

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

def zscore_df(df, var_list):
    """ 
    Takes DateFrame and z-scores values within each of the columns
    """
    scaler = StandardScaler()
    return scaler.fit_transform(df[var_list])