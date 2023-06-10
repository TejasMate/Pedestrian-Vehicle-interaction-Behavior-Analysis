"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
              #   Check Interaction between Pedestrian & Vehicles
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pandas as pd
import numpy as np
import matplotlib.path as mpath
import json

import pedonroad

def find(vehicles_df, pedes_df, map, map_coords_df):
    
    # Uses pedonroad.check function to return "Pedestrian on dataframe"
    # dataframe into ped_on_road_df
    ped_on_road_df = pedonroad.check(map, pedes_df)
        
    # Extracting all Pedestrian TrackIDs for future loop that
    # find compare interaction one by one pedestrian with
    # every vehicle 
    all_ped_trackids = np.unique(pedes_df['track_id'].to_numpy())
        
    # Loading json file of Polygon Coordinates of every Pedestrian
    # poly_coords dictionary
    with open('Generated Files/Polygon Coordinates of each Pedestrian.json', 'r') as f:
        poly_coords = json.load(f)    
    
    # Creating Empty Dataframe interact with column names: Pedestrian TrackID,
    # Vehicle TrackID, Timestamp
    interact = pd.DataFrame(columns =['Pedestrian TrackID', 'Vehicle TrackID', 'Timestamp'])


    for ped_track_id in all_ped_trackids:
        ped_row = ped_on_road_df[ped_on_road_df['Track ID'] == ped_track_id]
        
        x_var_keyname = str(ped_track_id+"x")
        y_var_keyname = str(ped_track_id+"y")
       
        x_coords = poly_coords[x_var_keyname]
        y_coords = poly_coords[y_var_keyname]
        
        vertices = list(zip(x_coords, y_coords))

        if len(vertices) == 0:
            continue
        
        path = mpath.Path(vertices)
        
        ped_start_ts = int(ped_row["Crossing start at TS"])
        ped_end_ts = int(ped_row["Crossing ends at TS"])
        
        total_ts= []
        
        for ts in range(ped_start_ts, ped_end_ts+100, 100):
            total_ts.append(ts)
            
        for ts in total_ts:
            same_ts_veh = vehicles_df[vehicles_df['timestamp_ms'] == ts]

            for row in range(0,len(same_ts_veh['track_id'])):
                veh_x = same_ts_veh.iloc[row,4]                                        # Column 4 -> x
                veh_y = same_ts_veh.iloc[row,5]                                        # Column 5 -> y
                veh_track_id= int(same_ts_veh.iloc[row,0])                              
                
                # Define the point coordinates to check
                point = (veh_x, veh_y)
        
                # Check if the point is inside the polygon
                is_inside = path.contains_point(point)
                
                if is_inside == True:
                    append_row = pd.DataFrame([{'Pedestrian TrackID': ped_track_id, 'Vehicle TrackID': veh_track_id, 'Timestamp': ts}])
                    interact = pd.concat([interact, append_row])  

    interact.to_csv("Generated Files/Interaction between Pedestrians and Vehicles.csv")
    
    return interact, ped_on_road_df, poly_coords