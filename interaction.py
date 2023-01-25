
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
              #   Check Interaction between Pedestrian & Vehicles
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
 def interact()   
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