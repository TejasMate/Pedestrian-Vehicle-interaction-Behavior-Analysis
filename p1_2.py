import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

interact_df = pd.read_csv("Generated Files/Interaction between Pedestrians and Vehicles.csv")
vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_001.csv", engine="pyarrow")
pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_001.csv", engine="pyarrow")

interact_2 = pd.DataFrame()
frame = 0

ped = "P1"
veh = 2

curr_veh_df = vehicles_df[vehicles_df['track_id'] == veh]
curr_ped_df = pedes_df[pedes_df['track_id'] == ped]

ped_ts = np.array(curr_ped_df['timestamp_ms']).astype(int)
veh_ts = np.array(curr_veh_df['timestamp_ms']).astype(int)

all_ts = np.sort(np.unique(np.concatenate([veh_ts,ped_ts])))
all_interact_ts = (interact_df.loc[(interact_df['Pedestrian TrackID'] == ped) & (interact_df['Vehicle TrackID'] == veh), 'Timestamp']).values
       

for ts in all_ts:
    
    match_ts_veh_row = curr_veh_df.loc[(curr_veh_df['timestamp_ms'] == ts)]
    match_ts_veh_row = match_ts_veh_row.squeeze()
    
    if match_ts_veh_row.empty:
        veh_x = veh_y = veh_vx = veh_vy = veh_speed = np.nan
    else:
        veh_x = match_ts_veh_row.x
        veh_y = match_ts_veh_row.y
        veh_vx = match_ts_veh_row.vx
        veh_vy = match_ts_veh_row.vy
        veh_speed = math.sqrt(veh_vx**2 + veh_vy**2)

    match_ts_ped_row = curr_ped_df.loc[(curr_ped_df['timestamp_ms'] == ts)]
    match_ts_ped_row = match_ts_ped_row.squeeze()
    
    if match_ts_ped_row.empty:
        ped_x = ped_y = ped_vx = ped_vy = ped_speed = np.nan
    else:
        ped_x = match_ts_ped_row.x
        ped_y = match_ts_ped_row.y
        ped_vx = match_ts_ped_row.vx
        ped_vy = match_ts_ped_row.vy
        ped_speed = math.sqrt(ped_vx**2 + ped_vy**2)

    if ts in all_interact_ts:
        interaction = 1
    else:
        interaction = 0
        
    if not (match_ts_ped_row.empty and match_ts_veh_row.empty):
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
            'Pedestrian Speed': ped_speed,
            'interaction': interaction, 
            'Vehicle TrackID': veh,
            'veh x': veh_x, 
            'veh y': veh_y,
            'veh vx': veh_vx, 
            'veh vy': veh_vy,
            'Vehicle Speed': veh_speed,
            'distance': distance
        }
    ])            
    interact_2 = pd.concat([interact_2, append_row]) 


y_min = interact_2['Vehicle Speed'].min() - 0.1
y_max = interact_2['Vehicle Speed'].max() + 0.1

new_interact_2 = interact_2.dropna(how='any')
new_interact_2.plot(x="Timestamp", y=["Pedestrian Speed", "Vehicle Speed"], kind="line")
new_interact_2.plot(x="Timestamp", y=["Pedestrian Speed", "Vehicle Speed"], kind="bar")
plt.title('Speed: Both Vehicle and Pedestrian Present at a TS')
plt.ylim(y_min, y_max)

y_min = interact_2['distance'].min() - 1
y_max = interact_2['distance'].max() + 5

new_interact_2 = interact_2.dropna(how='any')
new_interact_2.plot(x="Timestamp", y=["distance"], kind="line")
new_interact_2.plot(x="Timestamp", y=["distance"], kind="bar")
plt.title('Distance: When both Vehicle and Pedestrian Present at a Timestamp')
plt.ylim(y_min, y_max)

plt.show()


del veh_x, veh_y, veh_vx, veh_vy, veh_speed, ped_x, ped_y, ped_vx, ped_vy,  ped_speed, append_row, distance, ts, frame, match_ts_ped_row, match_ts_veh_row, interaction