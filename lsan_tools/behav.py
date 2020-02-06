import pandas as pd 
pd.options.mode.chained_assignment = None

__all__ = ['select_data',
           'scorer',
           'check_total_items',
           'retain_items',
           'join_data',
           'score_hexaco',
           'score_rel_mobility',
           'score_isel',
           'score_dospert',
           'score_stab'
           ]

__author__ = ["Shawn Rhoads","Katherine O'Connell","Kathryn Berluti"]

class survey(object):

    """ 
    The lsan_survey class allows users to easily perform a variety of different
    functions on questionnaires used in the Georgetown Laboratory of Social and 
    Affective Neuroscience.

    """

    def __init__(self,csv_file,index_col_name):
        self.data = pd.read_csv(csv_file, index_col=index_col_name)
        self.original_data = True
        self.index_col_name = index_col_name
        self.scored_data = {}


    def select_data(self, sub_ids, rewrite_to_self=False, save=True, filename="selected_data"):
        if type(sub_ids) != list:
            if type(sub_ids) != str:
                raise ValueError("`sub_ids` is not a list or string")
            else:
                print("\n`sub_ids` is a string, reading "+sub_ids+" from file\n")
                with open(sub_ids, 'r') as f:
                    selected_sub_ids = [int(x) for x in f.readlines()]
        else:
            selected_sub_ids = sub_ids 

        selected_data = self.data.loc[selected_sub_ids, :]

        if rewrite_to_self: # if we want to rewrite existing data to score selected data
            self.data = selected_data
            self.original_data = False
        else:
            if save:
                selected_data.to_csv(filename+".csv")
            else:
                return selected_data

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
            raise ValueError("Number of question items does not match the number of items specified! Please check your data and try again.")

    def retain_items(self, list):
        self.scored_data['other'] = self.data[list]

    def join_data(self, save=True, filename="scored_data"):
        if self.scored_data != {}:
            # loop through all scored data
            all_data = [scored_scale for scored_scale in self.scored_data.values()]
            joined_data = all_data[0].join(all_data[1:])
            
            if save:
                joined_data.to_csv(filename+".csv") #save to .csv unless otherwise specified
            else:
                return joined_data
        else:
            raise ValueError("User needs to score data before trying to join!")               

    def score_hexaco(self, scale_name = 'hexaco'):
        # initiate variables
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

    def score_rel_mobility(self, scale_name = 'relational_mobility'):
        # initiate variables
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
        subscales['relational_mobility'] = [n for n in range(1,13)]
        
        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(rel_mobility, scale_name, subscale_name, subscale_items)

    def score_isel(self, scale_name = 'isel'):
        # initiate variables
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

    def score_dospert(self, scale_name = 'dospert'):
        # initiate variables
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
        subscales['risk_taking_ethical'] = [6, 9, 10, 16, 29, 30]
        subscales['risk_taking_financial'] = [3, 4, 8, 12, 14, 18]
        subscales['risk_taking_health_safety'] = [5, 15, 17, 20, 23, 26]
        subscales['risk_taking_recreational'] = [2, 11, 13, 19, 24, 25]
        subscales['risk_taking_social'] = [1, 7, 21, 22, 27, 28]
        subscales['risk_perception_ethical'] = [36, 39, 40, 46, 59, 60]
        subscales['risk_perception_financial'] = [33, 34, 38, 42, 44, 48]
        subscales['risk_perception_health_safety'] = [35, 45, 47, 50, 53, 56, ]
        subscales['risk_perception_recreational'] = [32, 41, 43, 49, 54, 55]
        subscales['risk_perception_social'] = [31, 37, 51, 52, 57, 58]

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(dospert, scale_name, subscale_name, subscale_items)

    def score_stab(self, scale_name = 'STAB'):
        # initiate variables
        self.scored_data[scale_name] = pd.DataFrame()

        # check number of items on STAB (columns)
        self.check_total_items(scale_name, 33)
        
        # initiate df with STAB items only
        STAB = self.data.filter(regex=str(scale_name+"_"))    
        
        # reverse score items in scale
        max_scale = 3
        min_scale = 1
        reversed_items = []

        for i in reversed_items:
            STAB.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - STAB.loc[:,scale_name+"_"+str(i)] 
        # specify subscales
        subscales = {}
        subscales['phys'] = [2,5,8,11,14,17,20,23,26,29]
        subscales['soc'] = [4,7,10,13,16,19,22,25,28,31,33]
        subscales['rule'] = [3,6,9,12,15,18,21,24,27,30,32]

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(STAB, scale_name, subscale_name, subscale_items, calc_mean=False)