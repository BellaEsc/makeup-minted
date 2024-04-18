import pandas as pd
import re as re
import numpy as np
from IPython.display import display, clear_output

def ingredient_in_INCI(inci, ingredient_name):
    '''
    Takes two string arguments: an official INCI name, and an ingredient
    (as listed in the product dataframe). Returns True if every word in
    the ingredient name can be found in the INCI name. 

    This is a helper function used in get_shortest_INCI().
    '''

    # Removes whitespace and punctuation and puts text in lowercase
    cleaned_inci_text = re.sub(r'[^\w\s]', ' ', inci).lower() 
    cleaned_ingredient_text = re.sub(r'[^\w\s]', ' ', ingredient_name).lower()

    # Creates a set from the cleaned text which contains all of the words
    # in the cleaned up string
    words_in_inci = set(cleaned_inci_text.split())
    words_in_name = set(cleaned_ingredient_text.split())

    # Using set comparison: if the words in ingredient name are a subset
    # of the words in the inci name, return True. Otherwise, return False.
    return (words_in_name <= words_in_inci)



def get_shortest_INCI(df, ingredient_name):
    ''' 
    Takes the ingredients dataframe (df) and an ingredient name
    as arguments, then returns the matching row from the dataframe if
    a match is found. Otherwise, returns an empty row.
    '''

    # Uses ingredient_in_INCI to map and filter the df by whether the  given 
    # ingredient name matches an INCI name in the df. 
    filtered_df = \
        df[df['INCI name'].apply(lambda x: ingredient_in_INCI(x, ingredient_name))]
    
    # If no matches are found, try searching again but with removing words 
    # that are surrounded by parenthesis.
    if filtered_df.size == 0:
        ingredient_name_clean = re.sub(r'\([^)]*\)', '', ingredient_name)

        filtered_df = \
            df[df['INCI name'].apply(lambda x: ingredient_in_INCI(x, ingredient_name_clean))]
        
        # If there are still no matches, return null
        if filtered_df.size == 0:
            return np.nan

    # If there are multiple matches, return only the 
    # shortest INCI name's COSING Ref No. 
    shortest_index = filtered_df['INCI name'].str.len().idxmin()
    return filtered_df.loc[[shortest_index]]['COSING Ref No'].iloc[0]



def get_INCI_name_list(inci_df, ingredient_list):
    '''
    Takes a list of ingredients (as strings) as an argument,
    then returns a list of corresponding Cosing Ref No. Drops
    any ingredients that aren't found.
    '''
    new_list = np.array([get_shortest_INCI(inci_df, ingredient) for ingredient in ingredient_list])
    return new_list[~np.isnan(new_list)]
