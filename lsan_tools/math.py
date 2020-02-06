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

# def pairwise_vector(vec1, vec2, method="correlation", shuffle=False):
#     """
#     Takes a DateFrame and computes pairwise  
#     distance between two column vectors

#     Returns a 2D dissimilarity matrix as np.array
#     """
#     matrix = {}

#     for sub_id1 in df.index:
#         for sub_id2 in df.index:

#             # need to get pairwise subjects
#             sub1 = df.loc[sub_id]
#             sub2 = 

#         sub_pair = 

#         matrix[sub_pair] = {}

#         for variable in var_list:
#             sub1_vector = df[variable].loc[sub1]
#             sub2_vector = df[variable].loc[sub2]

#             # if one of the subjects is missing data for this variable, replace with NaN
#             if not sub1_vector or not sub2_vector:
#                 dist = np.nan

#             else:            
#                 X = np.array([sub1_vector, sub2_vector])
#                 dist = distance.pdist(X, metric=method)

#             matrix[sub_pair][variable] = float(dist) 

#     return matrix

def standardize(df, var_list):
    """ 
    Takes DateFrame and z-scores values within each of the columns
    """
    scaler = StandardScaler()
    return scaler.fit_transform(df[var_list])

