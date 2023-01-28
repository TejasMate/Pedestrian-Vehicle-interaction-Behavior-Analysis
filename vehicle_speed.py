"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                            # Vehicle Speed Calculation 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import pandas as pd

vehicles_avg_speed = pd.DataFrame(columns =["veh_track_id", "average speed"])

def speed(vehicles_df, all_veh_trackids):    
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
        temp1 = pd.DataFrame([{'veh_track_id' : v_trackid, 'average speed' : avgspeed}])
        global vehicles_avg_speed
        vehicles_avg_speed = pd.concat([vehicles_avg_speed, temp1], ignore_index = True)
    return vehicles_df, vehicles_avg_speed
