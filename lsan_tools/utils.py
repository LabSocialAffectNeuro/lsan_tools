import pandas as pd 
pd.options.mode.chained_assignment = None

__all__ = ['scorer',
           'check_total_items',
           'join_data',
           'score_hexaco',
           'score_rel_mobility',
           'score_isel',
           'score_dospert'
           ]
__author__ = ["Shawn Rhoads","Katherine O'Connell","Kathryn Berluti"]

class lsan_survey(object):

    """ 
    The lsan_survey class allows users to easily score a variety of different
    questionnaires used in the Georgetown Laboratory of Social and Affective
    Neuroscience.
    """

    def __init__(self,csv_file,index_col_name):
        self.data = pd.read_csv(csv_file, index_col=index_col_name)
        self.scored_data = {}

    def scorer(self, df, scale_name, subscale_names, subscale_items, calc_mean=True):
        ''' loads data from indicated scale, sums all subscale items, and takes mean (unless specified otherwise) '''
        item_list = [str(scale_name+"_") + s for s in [str(i) for i in subscale_items]]
        
        scored_df = pd.DataFrame(index = df.index)
        scored_df = df.loc[:,item_list].sum(axis=1)
            
        if calc_mean:
            scored_df = scored_df / len(item_list)
        
        return scored_df
    
    def check_total_items(self, scale_name, scale_total_items):
        if len(self.data.filter(regex=str(scale_name+"_")).columns) != scale_total_items:
            raise ValueError("Number of question items does not match the number of items specified!")

    def join_data(self,save=True):
        if self.scored_data != {}
            # loop through all scored data
            all_data = [scored_scale for scored_scale in self.scored_data.values()]
            joined_data = all_data[0].join(all_data[1:])
            
            if save:
                joined_data.to_csv("scored_data.csv") #save to .csv unless otherwise specified

            return joined_data
        else:
            raise ValueError("User needs to score data before trying to join!")               

    def score_hexaco(self):
        # initiate variables
        scale_name = 'hexaco'
        self.scored_data[scale_name] = pd.DataFrame()
        
        # check number of HEXACO total items (columns)
        self.check_total_items(scale_name, 60)
        
        # initiate df with HEXACO items only
        hexaco = self.data.filter(regex=str(scale_name+"_"))
        
        # reverse score items in scale
        max_scale = 5
        min_scale = 1
        reversed_items = [30, 12, 60, 42, 24, 48, 53, 35, 41, 59, 28, 52, 10, 46, 9, 15, 57, 21, 26, 32, 14, 20, 44, 56, 1, 31, 49, 19, 55]
        
        for i in reversed_items:
            hexaco.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - hexaco.loc[:,scale_name+"_"+str(i)] 
        
        # specify subscales
        subscales = {}
        subscales['honestyhumility'] = [6, 30, 54, 12, 36, 60, 18, 42, 24, 48]
        subscales['emotionality'] = [5, 29, 53, 11, 35, 17, 41, 23, 47, 59]
        subscales['extraversion'] = [4, 28, 52, 10, 34, 58, 16, 40, 22, 46]
        subscales['agreeableness'] = [3, 27, 9, 33, 51, 15, 39, 57, 21, 45]
        subscales['conscientiousness'] = [2, 26, 8, 32, 14, 38, 50, 20, 44, 56]
        subscales['openness'] = [1, 25, 7, 31, 13, 37, 49, 19, 43, 55]
        
        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(hexaco, scale_name, subscale_name, subscale_items)

    def score_rel_mobility(self):
        # initiate variables
        scale_name = 'relational_mobility'
        self.scored_data[scale_name] = pd.DataFrame()
        
        # check number of Relational Mobility total items (columns)
        self.check_total_items(scale_name, 12)
        
        # initiate df with Relational Mobility items only
        rel_mobility = self.data.filter(regex=str(scale_name+"_"))
        
        # reverse score items in scale
        max_scale = 6
        min_scale = 1
        reversed_items = [4, 5, 7, 9, 11, 12]

        for i in reversed_items:
            rel_mobility.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - rel_mobility.loc[:,scale_name+"_"+str(i)] 
        
        # specify subscales
        subscales = {}
        subscales['rel_mobility'] = [n for n in range(1,13)]
        
        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(rel_mobility, scale_name, subscale_name, subscale_items)

    def score_isel(self):
        # initiate variables
        scale_name = 'isel'
        self.scored_data[scale_name] = pd.DataFrame()

        # check number of Interpersonal Support Evaluation List (40-item) (columns)
        self.check_total_items(scale_name, 40)
        
        # initiate df with ISEL items only
        isel = self.data.filter(regex=str(scale_name+"_"))    
        
        # reverse score items in scale
        max_scale = 4
        min_scale = 0
        reversed_items = [3, 6, 9, 10, 11, 13, 14, 15, 17, 24, 25, 27, 28, 29, 30, 34, 35, 36, 39, 40]

        for i in reversed_items:
            isel.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - isel.loc[:,scale_name+"_"+str(i)] 

        # specify subscales
        subscales = {}
        subscales['appraisal'] = [1, 6, 11, 17, 19, 22, 26, 30, 36, 38]
        subscales['tangible'] = [2, 9, 14, 16, 18, 23, 29, 33, 35, 39]
        subscales['selfesteem'] = [3, 4, 8, 13, 20, 24, 28, 32, 37, 40]
        subscales['belonging'] = [5, 7, 10, 12, 15, 21, 25, 27, 31, 34]

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(isel, scale_name, subscale_name, subscale_items, calc_mean=False)

    def score_dospert(self):
        # initiate variables
        scale_name = 'dospert'
        self.scored_data[scale_name] = pd.DataFrame()

        # check number of dospert total items (columns) = 60
        self.check_total_items(scale_name, 60)

        # initiate df with dospert items only
        dospert = self.data.filter(regex=str(scale_name+"_"))

        # reverse score items in scale
        max_scale = 7 # scale = 1:7
        min_scale = 1
        reversed_items = []

        for i in reversed_items:
            dospert.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - dospert.loc[:,scale_name+"_"+str(i)]

        # specify subscales
        subscales = {}
        subscales['risk taking ethical'] = [6, 9, 10, 16, 29, 30]
        subscales['risk taking financial'] = [3, 4, 8, 12, 14, 18]
        subscales['risk taking health/saftey'] = [5, 15, 17, 20, 23, 26]
        subscales['risk taking recreational'] = [2, 11, 13, 19, 24, 25]
        subscales['risk taking social'] = [1, 7, 21, 22, 27, 28]
        subscales['risk perceptiong ethical'] = [36, 39, 40, 46, 59, 60]
        subscales['risk perceptiong financial'] = [33, 34, 38, 42, 44, 48]
        subscales['risk perceptiong health/saftey'] = [35, 45, 47, 50, 53, 56, ]
        subscales['risk perceptiong recreational'] = [32, 41, 43, 49, 54, 55]
        subscales['risk perceptiong social'] = [31, 37, 51, 52, 57, 58]

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(dospert, scale_name, subscale_name, subscale_items)
