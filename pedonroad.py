import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.neighbors import KDTree
import os
from scipy.spatial import KDTree

import osmtocoordinates
import files
import pedestrian_individual
import math

def pedpoly(center_x, center_y, range_size, mappoints): #mappoints is dataframe with x and y coordinates
         
    # Determine range axis based on range size and range of values in dataframe
    x_range = mappoints['x'].max() - mappoints['x'].min()
    y_range = mappoints['y'].max() - mappoints['y'].min()
    if x_range > y_range and range_size <= x_range:
        range_axis = 'x'
    elif y_range > x_range and range_size <= y_range:
        range_axis = 'y'
    else:
        print("Range size too large for any axis, please enter a smaller range size.")
        exit()
    
    # Filter dataframe to include only points within the specified range
    if range_axis == 'x':
        nearby_df = mappoints[(mappoints['x'] >= center_x - range_size) & (mappoints['x'] <= center_x + range_size)]
    elif range_axis == 'y':
        nearby_df = mappoints[(mappoints['y'] >= center_y - range_size) & (mappoints['y'] <= center_y + range_size)]
    
    # Find the two nearest points to the center point
    tree = KDTree(nearby_df[['x', 'y']])
    dist, ind = tree.query([[center_x, center_y]], k=2)
    
    # Fit a line to the two nearest points
    point1 = nearby_df.iloc[ind[0][0]]
    point2 = nearby_df.iloc[ind[0][1]]
    line_params = np.polyfit([point1['x'], point2['x']], [point1['y'], point2['y']], 1)
    
    # Get the nearby coordinates that lie on the line passing through the two nearest points
    if range_axis == 'x':
        line_nearby_df = nearby_df[np.abs(nearby_df['y'] - np.polyval(line_params, nearby_df['x'])) <= range_size]
        
        # Append center point to the dataframe
        center_row = pd.DataFrame({'x': [center_x], 'y': [center_y]})
        line_nearby_df = pd.concat([line_nearby_df, center_row])  
        
    elif range_axis == 'y':
        line_nearby_df = nearby_df[np.abs(nearby_df['x'] - np.polyval(line_params, nearby_df['y'])) <= range_size]
        
        # Append center point to the dataframe
        center_row = pd.DataFrame({'x': [center_x], 'y': [center_y]})
        line_nearby_df = pd.concat([line_nearby_df, center_row])  

    
    line_nearby_df = line_nearby_df.sort_values(by=range_axis)
           
    return line_nearby_df, range_axis

def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


#def check(map_path, local_pedes_df):
def check(map_coords_df, local_pedes_df, vehicle_df):

    if os.path.exists(f"{files.TRACKFILE_DATA}/Pedestrians on road.csv"):
        ped_on_road_df = pd.read_csv(f"{files.TRACKFILE_DATA}/Pedestrians on road.csv")
        df = pd.DataFrame()
        for idx, pedestrian_row in ped_on_road_df.iterrows():
            ped = pedestrian_row['Track ID']
            startts = pedestrian_row['Crossing start at TS']
            endts = pedestrian_row['Crossing ends at TS']
            veh = pedestrian_row['vid']
            dec = pedestrian_row['dvalue']

            curr_ped = local_pedes_df[(local_pedes_df['track_id'] == ped) & (local_pedes_df['timestamp_ms'] == startts)]
            print(pedestrian_row)
            print(curr_ped)
            startx= float(curr_ped['x'])
            starty =  float(curr_ped['y'])

            curr_ped = local_pedes_df[(local_pedes_df['track_id'] == ped) & (local_pedes_df['timestamp_ms'] == endts)]
            
            endx = float(curr_ped['x'])
            endy =  float(curr_ped['y'])
            
            lanewidth = math.sqrt((endx - startx)**2 + (endy - starty)**2)
            
            df2 = pd.DataFrame([{'Track ID': ped, 'Vehicle Track ID': veh, 'Crossing start X': startx, 'Crossing start Y': starty, 'Crossing start at TS': startts, 'Crossing ends X': endx, 'Crossing ends Y': endy, 'Crossing ends at TS': endts, 'Lanewidth': lanewidth, 'Decision': dec}])
            df = pd.concat([df, df2]) 
        dir=f"{files.TRACKFILE_DATA}/Pedestrians on roadss.csv"
        df.to_csv(dir)
        return ped_on_road_df
    else:
        ped_on_road_df = pd.DataFrame()
    
        ped_grp_by_trackid = local_pedes_df.groupby('track_id')
        all_ped_trackids = np.unique(local_pedes_df['track_id'].to_numpy())
                    
        for p_trackid in all_ped_trackids:
            curr_ped = ped_grp_by_trackid.get_group(p_trackid)
            
            # Convert xyz dataframe to a set of tuples containing x and y coordinates
            xyz_set = set([(round(x, 3), round(y, 3)) for x, y in zip(vehicle_df['x'], vehicle_df['y'])])
            
            # Iterate over curr_ped dataframe and remove matching coordinates
            for idx, pedestrian_row in curr_ped.iterrows():
                x_pedestrian = round(pedestrian_row['x'], 3)
                y_pedestrian = round(pedestrian_row['y'], 3)
                
                if (x_pedestrian, y_pedestrian) in xyz_set:
                    curr_ped.drop(idx, inplace=True)
            
            # Reduce decimal places to 2
            for idx, pedestrian_row in curr_ped.iterrows():
                x_pedestrian = round(pedestrian_row['x'], 2)
                y_pedestrian = round(pedestrian_row['y'], 2)
                
                if (x_pedestrian, y_pedestrian) in xyz_set:
                    curr_ped.drop(idx, inplace=True)
            
            # Reduce decimal places to 1
            for idx, pedestrian_row in curr_ped.iterrows():
                x_pedestrian = round(pedestrian_row['x'], 1)
                y_pedestrian = round(pedestrian_row['y'], 1)
                
                if (x_pedestrian, y_pedestrian) in xyz_set:
                    curr_ped.drop(idx, inplace=True)
                        
            map_coords_array = map_coords_df[['X', 'Y']].values
            
            kd_tree = KDTree(map_coords_array)
            
            start_row = None
            min_distance_start = float('inf')
            
            for _, pedestrian_row in curr_ped.iterrows():
                x_pedestrian = pedestrian_row['x']
                y_pedestrian = pedestrian_row['y']
            
                _, nearest_idx = kd_tree.query([(x_pedestrian, y_pedestrian)], k=1)
                nearest_coords = map_coords_array[nearest_idx][0]
            
                distance = calculate_distance(x_pedestrian, y_pedestrian, nearest_coords[0], nearest_coords[1])
                if distance < min_distance_start:
                    min_distance_start = distance
                    start_row = pedestrian_row
            
            start_row_index = start_row.name
            
            last_row = None
            min_distance_last = float('inf')
            
            # Exclude rows until the start row index and slice the start row if the DataFrame has at least one row
            if not curr_ped.empty:
                if len(curr_ped) > 1:
                    curr_ped = curr_ped.loc[start_row_index:].iloc[1:]
                start_row = curr_ped.iloc[0] if not curr_ped.empty else None
            
            for _, pedestrian_row in curr_ped.iloc[::-1].iterrows():
                x_pedestrian = pedestrian_row['x']
                y_pedestrian = pedestrian_row['y']
            
                _, nearest_idx = kd_tree.query([(x_pedestrian, y_pedestrian)], k=1)
                nearest_coords = map_coords_array[nearest_idx][0]
            
                distance = calculate_distance(x_pedestrian, y_pedestrian, nearest_coords[0], nearest_coords[1])
                if distance < min_distance_last:
                    min_distance_last = distance
                    last_row = pedestrian_row
            
            if start_row is None:
                print(p_trackid)
            else:
                print(p_trackid+" is crossing road from timestamp "+str(start_row['timestamp_ms'])+" to timestamp "+str(last_row['timestamp_ms']))
            
            start_ts = input("Enter timestamp when Pedestrian starts crossing the road: ")
            end_ts = input("Enter timestamp when Pedestrian ends crossing the road: ")

            """
            choice = input("Do you want to correct timestamps? \n Y or N: ")
            if choice == "Y":
                #pedestrian_individual.plot(ped_grp_by_trackid.get_group(p_trackid), map_coords_df)
                start_ts = input("Enter timestamp when Pedestrian starts crossing the road: ")
                end_ts = input("Enter timestamp when Pedestrian ends crossing the road: ")
            else:
                start_ts = start_row['timestamp_ms']
                end_ts = last_row['timestamp_ms']
            """
                
            append_row = pd.DataFrame([{'Track ID': p_trackid, 'Crossing start at TS': start_ts, 'Crossing ends at TS': end_ts}])
            ped_on_road_df = pd.concat([ped_on_road_df, append_row])  
            ped_on_road_df.to_csv(f"{files.TRACKFILE_DATA}/Pedestrians on road.csv")    
            
            

        #save.to_json(poly_coords)
    return ped_on_road_df