"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
              #   Check Interaction between Pedestrian & Vehicles
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pandas as pd
import math 




def interact(vehicles_df, pedes_df, all_veh_trackids, all_ped_trackids, ped_on_road_df):
        
    interact = pd.DataFrame(columns =['Pedestrian TrackID', 'Vehicle TrackID', 'Timestamp','Gap'])
    all_ped_ts = list()
    
    for row in range(0,len(ped_on_road_df)):
        startts = ped_on_road_df.iloc[row,3]
        endts = ped_on_road_df.iloc[row,6]
        
        for allts in range(startts, endts+100, 100):
            all_ped_ts.append(allts)
            
    for single_ts in all_ped_ts:
        same_ts_veh = vehicles_df[vehicles_df['timestamp_ms'] == single_ts]
        same_ts_ped = pedes_df[pedes_df['timestamp_ms'] == single_ts]  

        for row1 in range(0,len(same_ts_veh)):
            for row2 in range(0,len(same_ts_ped)):
                veh_x = same_ts_veh.iloc[row1, 4]
                veh_y = same_ts_veh.iloc[row1, 5]
                veh_trackid = same_ts_veh.iloc[row2, 0]
                
                ped_x = same_ts_ped.iloc[row2, 4]
                ped_y = same_ts_ped.iloc[row2, 5]
                ped_trackid = same_ts_ped.iloc[row2, 0]
                
                lower_x = ped_x-10 #upperleft_x = lowerleft_x
                higher_x = ped_x+10 #upperright_x = lowerright_x
                lower_y = ped_y-10 #lowerleft_y = lowerright_y
                higher_y = ped_y+10 #upperleft_y = upperright_y
                
                if veh_x>=lower_x and veh_x<=higher_x and veh_y>=lower_y and veh_y<=higher_y:
                    distance_gap = ((veh_x-ped_x)**2 + (veh_y-ped_y)**2)**0.5
                    add_row = pd.DataFrame([{'Pedestrian TrackID' : ped_trackid, "Vehicle TrackID": veh_trackid , 'Timestamp': single_ts, 'Gap': distance_gap}])
                    interact = pd.concat([interact, add_row], ignore_index = True)
                    
    interact.to_csv("interact.csv")
    return interact

    """
    for row in range(0,len(ped_on_road_df)):

        
        
        
        
    for row in range(0,len(ped_on_road_df)):
        startts = ped_on_road_df.iloc[row,3]
        endts = ped_on_road_df.iloc[row,6]

        for allts in range(startts, endts+100, 100):
            all_ped_ts.append(allts)
            
    for single_ts in all_ped_ts:
        same_ts_veh = vehicles_df[vehicles_df['timestamp_ms'] == single_ts]
        same_ts_ped = pedes_df[pedes_df['timestamp_ms'] == single_ts]
        
        for row1 in range(0,len(same_ts_veh)):
            for row2 in range(0,len(same_ts_ped)):
                ped_trackid = same_ts_ped.iloc[row2, 0]

                ped_status_on_road = ped_on_road_df[ped_on_road_df['Track ID'] == ped_trackid]

                
                veh_x = same_ts_veh.iloc[row1, 4]
                veh_y = same_ts_veh.iloc[row1, 5]
                veh_trackid = same_ts_veh.iloc[row2, 0]
    
        startx = ped_on_road_df.iloc[row,1]
        starty = ped_on_road_df.iloc[row,2]
        endx = ped_on_road_df.iloc[row,4]
        endy = ped_on_road_df.iloc[row,5]
            
    """

    """
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
    
    ######
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

