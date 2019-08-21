import pandas as pd 
import numpy as np 

class lsan_survey(object):

    def __init__(self):
        self.data = pd.DataFrame()
    
    def scorer(self, df, scale_name, subscale_names, subscale_items, calc_mean=True):
        item_list = [str(scale_name+"_") + s for s in [str(i) for i in subscale_items]]
        
        scored_df = pd.DataFrame(index = df.index)
        scored_df = df.loc[:,item_list].sum(axis=1)
            
        if calc_mean:
            scored_df = scored_df / len(item_list)
        
        return scored_df
    
    def score_hexaco(self):
        # initiate variables
        scale_name = 'hexaco'
        self.hexaco_scored = pd.DataFrame()
        
        # check if hexaco total items (columns) = 60
        if len(self.data.filter(regex=str(scale_name+"_")).columns) != 60:
            raise ValueError("Number of question items does not match the number of items specified!")
        
        # initiate df with HEXACO items only
        hexaco = self.data.filter(regex=str(scale_name+"_"))      
        
        # reverse score items in scale
        max_scale = 5 # scale = 1:5
        min_scale = 1
        reversed_items = [30,12,60,42,24,48,53,35,41,59,28,52,10,46,9,15,57,21,26,32,14,20,44,56,1,31,49,19,55]
        
        for i in reversed_items:
            hexaco.loc[:,'hexaco_' + str(i)] = (max_scale + min_scale) - hexaco['hexaco_' + str(i)] 
        
        # specify subscales
        subscales = {}
        subscales['hh'] = [6,30,54,12,36,60,18,42,24,48]
        subscales['emotionality'] = [5,29,53,11,35,17,41,23,47,59]
        subscales['extraversion'] = [4,28,52,10,34,58,16,40,22,46]
        subscales['agreeableness'] = [3,27,9,33,51,15,39,57,21,45]
        subscales['conscientiousness'] = [2,26,8,32,14,38,50,20,44,56]
        subscales['openness'] = [1,25,7,31,13,37,49,19,43,55]
        
        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.hexaco_scored[subscale_name] = self.scorer(hexaco, scale_name, subscale_name, subscale_items)