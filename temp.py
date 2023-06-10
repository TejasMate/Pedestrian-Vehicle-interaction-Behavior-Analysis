import pandas as pd
import numpy as np
import math

interact_df = pd.read_csv("C:/Users/tejas/Downloads/Interaction/Interaction (8)/Interaction/Generated Files/Interaction between Pedestrians and Vehicles.csv")
vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_000.csv", engine="pyarrow")
pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_000.csv", engine="pyarrow")

all_veh_trackids = np.sort(np.unique(interact_df['Vehicle TrackID']))
all_ped_trackids = np.sort(np.unique(interact_df['Pedestrian TrackID']))

interact = pd.DataFrame()
frame = 0


for ped in all_ped_trackids:
    curr_ped_df = pedes_df.loc[(pedes_df['track_id'] == ped)]

    interact_veh = interact_df.loc[(interact_df['Pedestrian TrackID'] == ped), 'Vehicle TrackID']
    interact_veh = np.sort(np.unique(interact_veh))
    
    for veh in interact_veh:
        curr_veh_df = vehicles_df.loc[(vehicles_df['track_id'] == veh)]

        all_ts = interact_df.loc[(interact_df['Pedestrian TrackID'] == ped) & (interact_df['Vehicle TrackID'] == veh), 'Timestamp']
        all_ts = all_ts.values
        
        for i in range(0,len(curr_ped_df)):
            row = curr_ped_df.iloc[i]

            ts = row.timestamp_ms
            ped_x = row.x
            ped_y = row.y
            ped_vx = row.vx
            ped_vy = row.vy
                        
            if ts in all_ts:
                interaction = 1
            else:
                interaction = 0
                
            match_ts_row = curr_veh_df.loc[(curr_veh_df['timestamp_ms'] == ts)]
            match_ts_row = match_ts_row.squeeze()

            if match_ts_row.empty:
                veh_x = veh_y = distance = veh_vx = veh_vy= 0
            else:
                veh_x = match_ts_row.x
                veh_y = match_ts_row.y
                veh_vx = match_ts_row.vx
                veh_vy = match_ts_row.vy

                distance = math.sqrt((veh_x - ped_x)**2 + (veh_y - ped_y)**2)
            
            frame+=1
            append_row = pd.DataFrame([
                {
                    'frame_id': frame, 
                    'Timestamp': ts, 
                    'Pedestrian TrackID': ped, 
                    'x': ped_x, 
                    'y': ped_y, 
                    'vx': ped_vx, 
                    'vy': ped_vy, 
                    'interaction': interaction, 
                    'Vehicle TrackID': veh,
                    'veh x': veh_x, 
                    'veh y': veh_y,
                    'veh vx': veh_vx, 
                    'veh vy': veh_vy,
                    'distance': distance
                }
            ])            
            interact = pd.concat([interact, append_row]) 


