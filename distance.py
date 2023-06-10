import numpy as np
import math

def find(pedestrian_df, vehicle_df):
    # Calculate distance between current and last x, y coordinates for each track_id
    last_x, last_y, last_track_id = {}, {}, None
    distances = []
    
    for index, row in vehicle_df.iterrows():
        track_id = row['track_id']
        x = row['x']
        y = row['y']
        
        # Check if track_id has a previous row
        if last_track_id is None or last_track_id != track_id:
            last_x[track_id] = x
            last_y[track_id] = y
            distances.append(np.nan)
        else:
            # Calculate distance
            distance = math.sqrt((x - last_x[track_id])**2 + (y - last_y[track_id])**2)
            distances.append(distance)
            last_x[track_id] = x
            last_y[track_id] = y
        
        last_track_id = track_id
        
    # Add distances to DataFrame
    vehicle_df['distance'] = distances
    
    
    # Calculate distance between current and last x, y coordinates for each track_id
    last_x, last_y, last_track_id = {}, {}, None
    distances = []
    
    for index, row in pedestrian_df.iterrows():
        track_id = row['track_id']
        x = row['x']
        y = row['y']
        
        # Check if track_id has a previous row
        if last_track_id is None or last_track_id != track_id:
            last_x[track_id] = x
            last_y[track_id] = y
            distances.append(np.nan)
        else:
            # Calculate distance
            distance = math.sqrt((x - last_x[track_id])**2 + (y - last_y[track_id])**2)
            distances.append(distance)
            last_x[track_id] = x
            last_y[track_id] = y
        
        last_track_id = track_id
        
    # Add distances to DataFrame
    pedestrian_df['distance'] = distances
    
    return pedestrian_df, vehicle_df