"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       # Plotting Vehicle, Pedestrian Data on Map
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Use map_vis_without_Lanelet library to visual Map
import map_vis_without_lanelet
import loader

def one(vehicles_df, pedes_df, interaction_in_short, map_path):
    
    # to subplot only one visual
    fig, axes = plt.subplots(1, 1)
    
    # Create Array of vehicles & pedestrian timestamp
    veh_ts = np.array(vehicles_df['timestamp_ms'], np.int64)
    ped_ts = np.array(pedes_df['timestamp_ms'], np.int64)
    min_ped_ts = np.min(ped_ts)-500
    all_timestamp_ms = np.sort(np.unique(np.concatenate((veh_ts,ped_ts))))
    all_timestamp_ms = all_timestamp_ms[all_timestamp_ms >= 16000]
    
    # Initialize prev_plot_veh & prev_plot_ped as Empty Dataframe
    # Use to store previously plotted data and reuse to plot
    prev_plot_veh = pd.DataFrame()
    prev_plot_ped = pd.DataFrame()
    
    # Run Loop one by one for all timestamps
    for ts in all_timestamp_ms:
    
        map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)  # Plot Map
        plt.title("Timestamp: " + str(ts))                                       # Give title to Map
        
        # Add vehicles_df row in veh_df if vehicles_df and Current Loop's Timestamp are same
        same_ts_veh_df = vehicles_df[vehicles_df['timestamp_ms'] == ts]
        
        # Add pedes_df row in ped_df if pedes_df and Current Loop's Timestamp are same
        same_ts_ped_df = pedes_df[pedes_df['timestamp_ms'] == ts]
    
        # Plot previously plotted vehicle & pedestrian coordinates to show highlighted 
        # route where vehicles is moved out
        prev_plot_veh = pd.concat([prev_plot_veh, same_ts_veh_df], ignore_index = True)
        plt.scatter(prev_plot_veh['x'], prev_plot_veh['y'], color="lightblue", s=prev_plot_veh['width'])
        
        prev_plot_ped = pd.concat([prev_plot_ped, same_ts_ped_df], ignore_index = True)
        plt.scatter(prev_plot_ped['x'], prev_plot_ped['y'], color="orange", s=2)    
        
        # Plot Vehicles coordinate as per current loop's timestamp
        plt.scatter(same_ts_veh_df['x'], same_ts_veh_df['y'], color="blue", s=same_ts_veh_df['width'])
        for row in range(0,len(same_ts_veh_df['track_id'])):
            x=same_ts_veh_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_veh_df.iloc[row,5]                                        # Column 5 -> y
            track_id= int(same_ts_veh_df.iloc[row,0])                           # Column 0 -> track_id
            """
            if type(same_ts_veh_df.iloc[row,11]) is np.float64:
                speed = str(round(same_ts_veh_df.iloc[row,11],2))
            else:
                speed = same_ts_veh_df.iloc[row,11]
            """
            plt.text(x, y+.5, str(track_id) , fontsize=7.5)
        
        # Plot Pedestrian coordinate as per current loop's timestamp
        plt.scatter(same_ts_ped_df['x'], same_ts_ped_df['y'], color="red", s=2)
        for row in range(0,len(same_ts_ped_df['track_id'])):
            x=same_ts_ped_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_ped_df.iloc[row,5]                                        # Column 5 -> y
            track_id= same_ts_ped_df.iloc[row,0]                                # Column 0 -> track_id
            plt.text(x+.1, y+1, track_id , fontsize=7.5)
            
            # Plot Pedestrian interaction with vehicles on X Axis Label
            plotinter = interaction_in_short[interaction_in_short['Pedestrian TrackID'] == track_id]
            string = str(list(plotinter['Vehicle TrackID']))
            plt.xlabel(str(track_id) + " can collide with vehicles: " + string)     
            
        plt.show()
        
        


def two(vehicles_df, pedes_df, interaction_in_short, map_path):
    
    # to subplot only one visual
    fig, axes = plt.subplots(1, 1)
    
    # Create Array of vehicles & pedestrian timestamp
    veh_ts = np.array(vehicles_df['timestamp_ms'], np.int64)
    ped_ts = np.array(pedes_df['timestamp_ms'], np.int64)
    min_ped_ts = np.min(ped_ts)-500
    all_timestamp_ms = np.sort(np.unique(np.concatenate((veh_ts,ped_ts))))
    all_timestamp_ms = all_timestamp_ms[all_timestamp_ms >= 16000]
    
    # Initialize prev_plot_veh & prev_plot_ped as Empty Dataframe
    # Use to store previously plotted data and reuse to plot
    prev_plot_veh = pd.DataFrame()
    prev_plot_ped = pd.DataFrame()

    i = 0
    
    # Run Loop one by one for all timestamps
    for ts in all_timestamp_ms:
        
        all_prev_plot_veh = pd.DataFrame()
        all_prev_plot_ped = pd.DataFrame()
        same_ts_veh_trackids = 0
        same_ts_ped_trackids = 0
        
        i+=1
        
        map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)  # Plot Map
        plt.title("Timestamp: " + str(ts))                                       # Give title to Map
        
   
        # Add vehicles_df row in veh_df if vehicles_df and Current Loop's Timestamp are same
        same_ts_veh_df = vehicles_df[vehicles_df['timestamp_ms'] == ts]
        #same_ts_veh_trackids = same_ts_veh_df["track_id"].to_numpy()
        same_ts_veh_trackids = np.array(same_ts_veh_df['track_id'],  np.int64)
        
        # Add pedes_df row in ped_df if pedes_df and Current Loop's Timestamp are same
        same_ts_ped_df = pedes_df[pedes_df['timestamp_ms'] == ts]
        same_ts_ped_trackids = np.array(same_ts_veh_df['track_id'],  np.int64)

        if i == 1:
            pass
        elif i<11:
            for prevts in range((ts-(i-1)*100), ts , 100):
                prev_plot_veh = vehicles_df[vehicles_df['timestamp_ms'] == prevts]
                
                for prev_veh_tids in same_ts_veh_trackids:
                    prev_plot_veh = prev_plot_veh[prev_plot_veh['track_id'] != prev_veh_tids]
                
                all_prev_plot_veh = pd.concat([all_prev_plot_veh, prev_plot_veh], ignore_index = True)
            plt.scatter(all_prev_plot_veh['x'], all_prev_plot_veh['y'], color="lightblue", s=all_prev_plot_veh['width'])
            print(all_prev_plot_veh)
        else:
            for prevts in range(ts-1000, ts , 100): 
                prev_plot_veh = vehicles_df[vehicles_df['timestamp_ms'] == prevts]
                
                for prev_veh_tids in same_ts_veh_trackids:
                    prev_plot_veh = prev_plot_veh[prev_plot_veh['track_id'] != prev_veh_tids]

                all_prev_plot_veh = pd.concat([all_prev_plot_veh, prev_plot_veh], ignore_index = True)
            plt.scatter(all_prev_plot_veh['x'], all_prev_plot_veh['y'], color="lightblue", s=all_prev_plot_veh['width'])
            print(all_prev_plot_veh)


        
        prev_plot_ped = pd.concat([prev_plot_ped, same_ts_ped_df], ignore_index = True)
        plt.scatter(prev_plot_ped['x'], prev_plot_ped['y'], color="orange", s=2)    
        
        # Plot Vehicles coordinate as per current loop's timestamp
        plt.scatter(same_ts_veh_df['x'], same_ts_veh_df['y'], color="blue", s=same_ts_veh_df['width'])
        for row in range(0,len(same_ts_veh_df['track_id'])):
            x=same_ts_veh_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_veh_df.iloc[row,5]                                        # Column 5 -> y
            track_id= int(same_ts_veh_df.iloc[row,0])                           # Column 0 -> track_id
            """
            if type(same_ts_veh_df.iloc[row,11]) is np.float64:
                speed = str(round(same_ts_veh_df.iloc[row,11],2))
            else:
                speed = same_ts_veh_df.iloc[row,11]
            """
            plt.text(x, y+.5, str(track_id) , fontsize=7.5)
        
        # Plot Pedestrian coordinate as per current loop's timestamp
        plt.scatter(same_ts_ped_df['x'], same_ts_ped_df['y'], color="red", s=2)
        for row in range(0,len(same_ts_ped_df['track_id'])):
            x=same_ts_ped_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_ped_df.iloc[row,5]                                        # Column 5 -> y
            track_id= same_ts_ped_df.iloc[row,0]                                # Column 0 -> track_id
            plt.text(x+.1, y+1, track_id , fontsize=7.5)
            
            # Plot Pedestrian interaction with vehicles on X Axis Label
            plotinter = interaction_in_short[interaction_in_short['Pedestrian TrackID'] == track_id]
            string = str(list(plotinter['Vehicle TrackID']))
            plt.xlabel(str(track_id) + " can collide with vehicles: " + string)     
            
        plt.show()