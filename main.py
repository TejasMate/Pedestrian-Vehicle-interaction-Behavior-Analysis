import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


# Use map_vis_without_Lanelet library to visual Map
import map_vis_without_lanelet
import loader
import plot

# Path of Map, Pedestrian & Vehicle Datasets
map_path = 'maps/DR_DEU_Roundabout_OF.osm'
map_path = loader.getmappath()

#pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_000.csv")
pedes_df = pd.read_csv(loader.getpeddspath())

#vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_000.csv")
vehicles_df = pd.read_csv(loader.getvehdspath())



vehicles_df['speed'] = ''

all_veh_trackids = np.unique(vehicles_df['track_id'].to_numpy())
all_ped_trackids = np.unique(pedes_df['track_id'].to_numpy())

vehicles_avg_speed = pd.DataFrame(columns =["veh_track_id", "average speed"])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
fig, axes = plt.subplots(1, 1)
map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)
mappoints = map_vis_without_lanelet.getpoints()
map_vis_without_lanelet.removefile()

pedstartx = []
pedstarty = []
pedstartts = []
pedendx = []
pedendy = []
pedendts = []
startx = ''
starty = ''
startts = ''
endx = ''
endy = ''
endts = ''

for p_trackid in all_ped_trackids:
    curr_ped = pedes_df[pedes_df['track_id'] == p_trackid]  
    
    for pedrow in range(0, len(curr_ped)-1):
        outerloop = 0

        for maprow in range(0, len(mappoints)-1):
            ped_x = round(curr_ped.iloc[pedrow,4])
            ped_y = round(curr_ped.iloc[pedrow,5])
            map_x = round(mappoints.iloc[maprow,1])
            map_y = round(mappoints.iloc[maprow,2])
  
            if (ped_x == map_x) and (ped_y == map_y):
                startx = curr_ped.iloc[pedrow,4]
                starty = curr_ped.iloc[pedrow,5]
                startts = curr_ped.iloc[pedrow,2]
                outerloop = 1
                break
                
        if outerloop == 1:
            break
            
    for pedrow in range(len(curr_ped)-1, 0, -1):
        outerloop = 0

        for maprow in range(len(mappoints)-1, 0, -1):
            ped_x = round(curr_ped.iloc[pedrow,4])
            ped_y = round(curr_ped.iloc[pedrow,5])
            map_x = round(mappoints.iloc[maprow,1])
            map_y = round(mappoints.iloc[maprow,2])
            
            if (ped_x == map_x) and (ped_y == map_y):
                endx = curr_ped.iloc[pedrow,4]
                endy = curr_ped.iloc[pedrow,5]
                endts = curr_ped.iloc[pedrow,2]
                outerloop = 1
                break
                
        if outerloop == 1:
            break
    
    pedstartx.append(startx)
    pedstarty.append(starty)
    pedstartts.append(startts)
    pedendx.append(endx)
    pedendy.append(endy)
    pedendts.append(endts)
    
tempdict = {'Track ID': all_ped_trackids, 'Crossing starts at X': pedstartx, 'Crossing starts at Y': pedstarty, 'Crossing start at TS': pedstartts ,'Crossing ends at X': pedendx, 'Crossing ends at Y': pedendy, 'Crossing ends at TS': pedendts}
df = pd.DataFrame(tempdict)
df.to_csv("PedonMap.csv")
    
    
    





"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                            # Vehicle Speed Calculation 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# track_id will be P1...P8
for v_trackid in all_veh_trackids:     
          
    # Current Track_id is match with every row track_id added in curr_veh
    curr_veh = vehicles_df[vehicles_df['track_id'] == v_trackid]   

    # empty list is created to add last 10 timestamp's calculated distance
    last_ten_ts = list()
    
    totalspeed = 0
    # First frame id of current track_id will store in first_frame
    # First frame is starting point, so vehicle not travelled any distance
    # first_frame will be avoided in inner for loop of all frames of current track_id
    first_frame = curr_veh.iloc[0,1]
    
    #One by one frame_id will go through for loop to calculate distance
    for i in range(0,len(curr_veh)):
        one_sec_convert = 0
        #speed = 0
        speedinkmph = 0
        
        if curr_veh.iloc[i,1] > first_frame:
            
            #Calculate distance between 2 points
            x1 = curr_veh.iloc[i-1,4]
            y1 = curr_veh.iloc[i-1,5]
            x2 = curr_veh.iloc[i,4]
            y2 = curr_veh.iloc[i,5]
        
            distance = (((x2-x1)**2) + ((y2-y1)**2))**0.5
            
            # Add last 10 timestamp's distance (1 timestamp = 100ms) in list of 10 elements
            if len(last_ten_ts) < 10:
                for d in range(0,10-len(last_ten_ts)):
                    last_ten_ts.append(distance)
            elif len(last_ten_ts) >= 10:
                last_ten_ts.pop(0)
                last_ten_ts.append(distance)
            
            # Add total 10 distance elements of 10 timestamps list to make 1 second distance
            for x in last_ten_ts:
                one_sec_convert += x
                
            # 1 Second per meter speed converted into Kilometer per hour
            speedinkmph = round((one_sec_convert*60*60/1000),3)
            totalspeed = totalspeed+speedinkmph
            # code to add speed value into vehicle dataframe
            index = vehicles_df.loc[(vehicles_df['frame_id'] == curr_veh.iloc[i,1]) & (vehicles_df['track_id'] == v_trackid)].index.to_numpy()                    
            vehicles_df.iloc[index,11] = speedinkmph
                
    avgspeed = totalspeed/(len(curr_veh)-1)
    temp2 = pd.DataFrame([{'veh_track_id' : v_trackid, 'average speed' : avgspeed}])
    vehicles_avg_speed = pd.concat([vehicles_avg_speed, temp2], ignore_index = True)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
              #   Check Interaction between Pedestrian & Vehicles
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

interact = pd.DataFrame(columns =['Pedestrian TrackID', 'Vehicle TrackID', 'Timestamp','Gap', 'Speed'])                

for p_trackid in all_ped_trackids:
    curr_ped = pedes_df[pedes_df['track_id'] == p_trackid]  
    
    for row in range(0,len(curr_ped)):
        curr_ped_ts = curr_ped.iloc[row,2]
        x1 = curr_ped.iloc[row,4]
        y1 = curr_ped.iloc[row,5]
        
        same_ts_veh_df = vehicles_df[vehicles_df['timestamp_ms'] == curr_ped_ts]  
        
        for vrow in range(0,len(same_ts_veh_df)):
            x2 = same_ts_veh_df.iloc[vrow,4]
            y2 = same_ts_veh_df.iloc[vrow,5]
            v_trackid = same_ts_veh_df.iloc[vrow,0]
            
            distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
            
            if distance <= 5:
                index = int(vehicles_df.loc[(vehicles_df['timestamp_ms'] == curr_ped_ts) & (vehicles_df['track_id'] == v_trackid)].index.to_numpy())
                speed = vehicles_df.iloc[index,11]
                add_row = pd.DataFrame([{'Pedestrian TrackID' : p_trackid, "Vehicle TrackID": v_trackid , 'Timestamp': curr_ped_ts, 'Gap': distance, 'Speed': speed}])
                interact = pd.concat([interact, add_row], ignore_index = True)



interaction_in_short = pd.DataFrame(columns =['Pedestrian TrackID', 'Vehicle TrackID', 'Interaction duration', 'Start Timestamp', 'Last Timestamp', 'Minimum Gap (timestamp)', 'Minimum Gap (speed)', 'Maximum Gap (timestamp)', 
                               'Maximum Gap (speed)', 'Minimum Speed (timestamp)', 'Maximum Speed (timestamp)', 'Average Speed of Vehicle'])
"""
row_read = 0
for ptrack_id in all_ped_trackids:
    for vtrack_id in all_veh_trackids:
        match = interact.loc[(interact['Pedestrian TrackID'] == ptrack_id) & (interact['Vehicle TrackID'] == vtrack_id)]
        
        if not match.empty:
            timestamps = np.unique(match['Timestamp'].to_numpy())
            gap = np.unique(match['Gap'].to_numpy())
            speed = np.unique(match['Speed'].to_numpy())

            Interaction_duration = (len(timestamps) * 100) - 100
            
            timestamps_max = timestamps.max()
            timestamps_min = timestamps.min()
            ind = 0
            
            gap_min = gap.min()
            index = int(match.loc[(match['Gap'] == gap_min)].index.to_numpy())  - row_read
            gap_min_ts = match.iloc[index,2]
            gap_min_ts = str(gap_min) + " ("  + str(gap_min_ts) + ")"
            gap_min_speed = match.iloc[index,4]
            gap_min_speed = str(gap_min) + " ("  + str(gap_min_speed) + ")"

            gap_max = gap.max()
            index = int(match.loc[(match['Gap'] == gap_max)].index.to_numpy()) - row_read
            gap_max_ts = match.iloc[index,2]
            gap_max_ts = str(gap_max) + " ("  + str(gap_max_ts)+")"
            gap_max_speed = match.iloc[index,4]
            gap_max_speed = str(gap_max) + " ("  + str(gap_max_speed) + ")"

            speed_min = speed.min()
            index = int(match.loc[(match['Speed'] == speed_min)].index.to_numpy()) - row_read
            speed_min_ts = match.iloc[index,2]
            
            speed_max = speed.max()
            index = int(match.loc[(match['Speed'] == speed_max)].index.to_numpy()) - row_read
            speed_max_ts = match.iloc[index,2]
            
            speed_avg = np.average(speed)
            
            add_row = pd.DataFrame([{'Pedestrian TrackID' : ptrack_id, "Vehicle TrackID": vtrack_id ,  'Interaction duration': Interaction_duration , 'Start Timestamp': timestamps_min, 'Last Timestamp': timestamps_max, 'Minimum Gap (timestamp)': gap_min_ts,  'Minimum Gap (speed)': gap_min_speed,
                                     'Maximum Gap (timestamp)': gap_max_ts,  'Maximum Gap (speed)': gap_max_speed, 'Minimum Speed (timestamp)' : speed_min_ts, 'Maximum Speed (timestamp)' : speed_max_ts, 'Average Speed of Vehicle' : speed_avg}])
            
            interaction_in_short = pd.concat([interaction_in_short, add_row], ignore_index = True)
            
            row_read = row_read + len(match)

interact.to_csv("interact.csv")
interaction_in_short.to_csv("file1.csv")

"""


# Plot only current trajectory without any Past/Future trajectories of every Pedestrian & Vehicle
# plot.one(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with Previous 10 and Next 10 trajectories of every Pedestrian & Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)
"""
# Plot current trajectory with Previous 10 and Next 10 trajectories of only of Pedestrian
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with Previous 10 and Next 10 trajectories of only of Vehicles
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all past trajectories of every Pedestrian & Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all past trajectories and next future 10 trajectories of every Pedestrian & Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all past trajectories and next future 10 trajectories of only of Pedestrian
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all past trajectories and next future 10 trajectories of only of Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)


# Plot current trajectory with all future trajectories of every Pedestrian & Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all future trajectories and previous past 10 trajectories of every Pedestrian & Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all future trajectories and previous past 10 trajectories of only of Pedestrian
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with all future trajectories and previous past 10 trajectories of only of Vehicle
plot.two(vehicles_df, pedes_df, interaction_in_short, map_path)

"""



