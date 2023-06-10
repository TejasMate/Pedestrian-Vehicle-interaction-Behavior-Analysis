"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                            # Vehicle Speed Calculation 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import math

def find(pedestrian_df, vehicles_df):    
    
    vehicles_df['speed'] = vehicles_df.apply(lambda row: math.sqrt(row['vx']**2 + row['vy']**2), axis=1)
    pedestrian_df['speed'] = pedestrian_df.apply(lambda row: math.sqrt(row['vx']**2 + row['vy']**2), axis=1)

    return pedestrian_df, vehicles_df