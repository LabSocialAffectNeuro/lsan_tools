import os
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
           'score_stab',
           'score_iri',
           'score_ppi_short'
           ]

__author__ = ["Shawn Rhoads","Katherine O'Connell","Kathryn Berluti"]

class survey(object):

    """ 
    The lsan_survey class allows users to easily perform a variety of different
    functions on questionnaires used in the Georgetown Laboratory of Social and 
    Affective Neuroscience.

    """

    def __init__(self,filename,index_col_name,xlsx_args=None):
        if isinstance(filename, pd.DataFrame):
            self.data = filename
        else:
            if os.path.splitext(filename)[-1] == '.csv':
                self.data = pd.read_csv(filename, index_col=index_col_name)
            elif os.path.splitext(filename)[-1] == '.xlsx':
                assert type(xlsx_args)==dict, ("Please specify xlsx_args for pandas.read_excel(): e.g., xlsx_args={\'sheet_name\':\"SHEET\"}")
                self.data = pd.read_excel(filename, index_col=index_col_name, sheet_name=xlsx_args['sheet_name'])

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
        num_items_present = len(self.data.filter(regex=str(scale_name+"_")).columns)
        if num_items_present != scale_total_items:
            raise ValueError(f"Number of question items ({num_items_present}) does not match the number of items specified! Please check your data and try again.")

    def retain_items(self, list=None):
        if list==None:
            self.scored_data['other'] = self.data
        else:
            self.scored_data['other'] = self.data[list]

    def join_data(self, save=True, filename="scored_data", filetype="csv", sep=","):
        if self.scored_data != {}:
            # loop through all scored data
            all_data = [scored_scale for scored_scale in self.scored_data.values()]
            joined_data = all_data[0].join(all_data[1:])
            
            if save:
                if filetype == "csv":
                    joined_data.to_csv(filename+".csv", sep=sep) #save to .csv unless otherwise specified
                elif filetype == "excel":
                    joined_data.to_excel(filename+".xlsx", sheet_name=filename)
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
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(hexaco, scale_name, subscale_name, subscale_items, calc_mean=True)

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
        subscales['relational_mobility'] = list(range(1,13))
        
        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(rel_mobility, scale_name, subscale_name, subscale_items, calc_mean=True)

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
        subscales['risk_perception_health_safety'] = [35, 45, 47, 50, 53, 56]
        subscales['risk_perception_recreational'] = [32, 41, 43, 49, 54, 55]
        subscales['risk_perception_social'] = [31, 37, 51, 52, 57, 58]

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(dospert, scale_name, subscale_name, subscale_items, calc_mean=True)

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
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(STAB, scale_name, subscale_name, subscale_items, calc_mean=True)

    def score_iri(self, scale_name = 'iri'):
        # initiate variables
        self.scored_data[scale_name] = pd.DataFrame()

        # check number of Interpersonal Reactivity Index items (28-item) (columns)
        self.check_total_items(scale_name, 28)
        
        # initiate df with IRI items only
        iri = self.data.filter(regex=str(scale_name+"_"))    
        
        # reverse score items in scale
        max_scale = 5
        min_scale = 1
        reversed_items = [3, 4, 7, 12, 13, 14, 15, 18, 19]

        for i in reversed_items:
            iri.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - iri.loc[:,scale_name+"_"+str(i)] 

        # specify subscales
        subscales = {}
        subscales['perspective_taking'] = [3, 8, 11, 15, 21, 25, 28]
        subscales['fantasy'] = [1, 5, 7, 12, 16, 23, 26]
        subscales['empathic_concern'] = [2, 4, 9, 14, 18, 20, 22]
        subscales['personal_distress'] = [6, 10, 13, 17, 19, 24, 27]

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(iri, scale_name, subscale_name, subscale_items, calc_mean=False)

    def score_ppi_short(self, scale_name = 'ppi_short'):
        # initiate variables
        self.scored_data[scale_name] = pd.DataFrame()

        # check number of Psychopathic Personality Inventory - Short items (56-item) (columns)
        self.check_total_items(scale_name, 56)
        
        # initiate df with PPI-short items only
        ppi = self.data.filter(regex=str(scale_name+"_"))

        # reverse score items in scale
        max_scale = 4
        min_scale = 1
        reversed_items = [1, 3, 8, 10, 11, 12, 19, 20, 25, 26, 27, 28, 32, 33, 37, 39, 40, 42, 45, 48, 49, 51, 54, 55]

        for i in reversed_items:
            ppi.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - ppi.loc[:,scale_name+"_"+str(i)] 

        # specify subscales
        subscales = {}
        subscales['machievellian_egocentricity'] = [7, 14, 23, 35, 43, 46, 56]
        subscales['social_influence'] = [8, 15, 17, 18, 21, 29, 32]
        subscales['fearlessness'] = [1, 4, 9, 19, 22, 38, 52]
        subscales['rebellious_nonconformity'] = [2, 5, 16, 30, 36, 47, 53]
        subscales['blame_externalization'] = [6, 24, 31, 34, 41, 44, 50]
        subscales['carefree_nonplanfulness'] = [20, 33, 40, 42, 49, 51, 54]
        subscales['stress_immunity'] = [3, 11, 13, 26, 28, 39, 48]

        subscales['coldheartedness'] = [10, 12, 25, 27, 37, 45, 55]
        subscales['selfcentered_impulsivity'] = [7, 14, 23, 35, 43, 46, 56, 2, 5, 16, 30, 36, 47, 53, 6, 24, 31, 34, 41, 44, 50, 20, 33, 40, 42, 49, 51, 54]
        subscales['fearless_dominance'] = [8, 15, 17, 18, 21, 29, 32, 1, 4, 9, 19, 22, 38, 52, 3, 11, 13, 26, 28, 39, 48]

        subscales['total'] = list(range(1,56))

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(ppi, scale_name, subscale_name, subscale_items, calc_mean=False)

    def score_ppi_long(self, scale_name = 'ppi_long'):
        # initiate variables
        self.scored_data[scale_name] = pd.DataFrame()

        # check number of Psychopathic Personality Inventory - Long items (154-item) (columns)
        self.check_total_items(scale_name, 154)
        
        # initiate df with PPI-short items only
        ppi = self.data.filter(regex=str(scale_name+"_"))

        # reverse score items in scale
        max_scale = 4
        min_scale = 1
        reversed_items = [3, 5, 6, 9, 10, 17, 21, 22, 24, 27, 28, 30, 31, 38, 44, 47, 50, 51, 53, 59, 65, 68, 69, 71, 72, 73, 74, 75, 76, 79, 82, 83, 86, 87, 88, 89, 97, 98, 99, 100, 101, 106, 108, 109, 110, 113, 117, 119, 120, 121, 123, 124, 128, 129, 130, 133, 135, 141, 142, 143, 145, 146, 152, 153]

        for i in reversed_items:
            ppi.loc[:,scale_name+"_"+str(i)] = (max_scale + min_scale) - ppi.loc[:,scale_name+"_"+str(i)] 

        # specify subscales
        subscales = {}
        subscales['machievellian_egocentricity'] = [1, 11, 17, 23, 33, 39, 45, 55, 61, 67, 77, 83, 92, 103, 114, 125, 132, 136, 147, 154]
        subscales['social_influence'] = [2, 21, 22, 24, 34, 41, 43, 46, 56, 63, 65, 68, 78, 85, 87, 91, 113, 135]
        subscales['fearlessness'] = [3, 12, 13, 25, 35, 47, 57, 69, 79, 93, 115, 126, 137, 148]
        subscales['rebellious_nonconformity'] = [4, 14, 15, 26, 36, 48, 58, 70, 80, 94, 104, 105, 116, 127, 138, 149]
        subscales['blame_externalization'] = [16, 18, 19, 38, 40, 60, 62, 82, 84, 90, 100, 112, 122, 134, 144] 
        subscales['carefree_nonplanfulness'] = [7, 29, 44, 51, 66, 73, 88, 89, 99, 101, 108, 111, 121, 123, 130, 133, 143, 145, 152]
        subscales['stress_immunity'] = [6, 10, 28, 32, 50, 54, 72, 76, 96, 118, 119, 140, 141]
        subscales['deviant_responding'] = [8, 30, 52, 74, 102, 107, 124, 129, 146, 151]
        subscales['virtuous_responding'] = [20, 37, 42, 59, 64, 81, 86, 95, 106, 117, 128, 139, 150]

        subscales['coldheartedness'] = [5, 9, 27, 31, 49, 53, 71, 75, 97, 98, 109, 110, 120, 131, 142, 153]
        subscales['selfcentered_impulsivity'] = [1, 11, 17, 23, 33, 39, 45, 55, 61, 67, 77, 83, 92, 103, 114, 125, 132, 136, 147, 154] + [4, 14, 15, 26, 36, 48, 58, 70, 80, 94, 104, 105, 116, 127, 138, 149] + [16, 18, 19, 38, 40, 60, 62, 82, 84, 90, 100, 112, 122, 134, 144] + [7, 29, 44, 51, 66, 73, 88, 89, 99, 101, 108, 111, 121, 123, 130, 133, 143, 145, 152]
        subscales['fearless_dominance'] = [2, 21, 22, 24, 34, 41, 43, 46, 56, 63, 65, 68, 78, 85, 87, 91, 113, 135] + [3, 12, 13, 25, 35, 47, 57, 69, 79, 93, 115, 126, 137, 148] +[6, 10, 28, 32, 50, 54, 72, 76, 96, 118, 119, 140, 141]

        subscales['total'] = list(range(1,154))

        # score each subscale and store in new dataframe
        for subscale_name, subscale_items in subscales.items():
            self.scored_data[scale_name].loc[:,str(scale_name+"_"+subscale_name)] = self.scorer(ppi, scale_name, subscale_name, subscale_items, calc_mean=False)
