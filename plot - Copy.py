"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       # Plotting Vehicle, Pedestrian Data on Map
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Use map_vis_without_Lanelet library to visual Map
import map_vis_without_lanelet

def getpolycoords(track_id, coords):
    x_var_keyname = str(track_id+"x")
    y_var_keyname = str(track_id+"y")
   
    x_coords = coords[x_var_keyname]
    y_coords = coords[y_var_keyname]

    return x_coords, y_coords
 
def visualize(vehicles_df, pedes_df, ped_on_road_df, interaction_in_short, map_path, coords):
    
    # to subplot only one visual
    fig, axes = plt.subplots(1, 1)
    
    # Create Array of vehicles & pedestrian timestamp
    veh_ts = np.array(vehicles_df['timestamp_ms'], np.int64)
    ped_ts = np.array(pedes_df['timestamp_ms'], np.int64)
    all_timestamp_ms = np.sort(np.unique(np.concatenate([veh_ts,ped_ts])))
    all_timestamp_ms = all_timestamp_ms[all_timestamp_ms >= 100]
    
    # Initialize prev_plot_veh & prev_plot_ped as Empty Dataframe
    # Use to store previously plotted data and reuse to plot
    prev_plot_veh = prev_plot_ped = pd.DataFrame()
    
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
        
        for rowveh in range(0, len(same_ts_veh_df)):
            plt.scatter(same_ts_veh_df['x'], same_ts_veh_df['y'], color="blue", s=same_ts_veh_df['width'])
        
        for row in range(0,len(same_ts_veh_df['track_id'])):
            x=same_ts_veh_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_veh_df.iloc[row,5]                                        # Column 5 -> y
            track_id= int(same_ts_veh_df.iloc[row,0])                           # Column 0 -> track_id
            plt.text(x, y+.5, str(track_id) , fontsize=7.5)
        
        # Plot Pedestrian coordinate as per current loop's timestamp
        plt.scatter(same_ts_ped_df['x'], same_ts_ped_df['y'], color="red", s=2)
        
        for row in range(0,len(same_ts_ped_df['track_id'])):
            x=same_ts_ped_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_ped_df.iloc[row,5]                                        # Column 5 -> y
            track_id= same_ts_ped_df.iloc[row,0]                                # Column 0 -> track_id
            plt.text(x+.1, y+1, track_id , fontsize=7.5)
            
            xs, ys = getpolycoords(track_id, coords)
            plt.plot(xs,ys)            
            
        plt.show()