import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import map_vis_without_lanelet

#def plot(interact_onepair, vehicles_df, pedes_df):
def plot(vehicles_df, pedes_df):

    #ped = interact_onepair.iloc[0]['Pedestrian TrackID']
    #veh = interact_onepair.iloc[0]['Vehicle TrackID']
    ped= "P9"
    veh= 35
    
    map_path = "maps/DR_USA_Intersection_EP0.osm"
    pedes_df = pd.read_csv("recorded_trackfiles/DR_USA_Intersection_EP0/pedestrian_tracks_000.csv", engine="pyarrow")
    vehicles_df = pd.read_csv("recorded_trackfiles/DR_USA_Intersection_EP0/vehicle_tracks_000.csv", engine="pyarrow")     
    
    curr_veh_df = vehicles_df[vehicles_df['track_id'] == veh]
    curr_ped_df = pedes_df[pedes_df['track_id'] == ped]
    
    # Create Array of vehicles & pedestrian timestamp
    veh_ts = np.array(curr_veh_df['timestamp_ms'], np.int64)
    ped_ts = np.array(curr_ped_df['timestamp_ms'], np.int64)
    all_timestamp_ms = np.sort(np.unique(np.concatenate([veh_ts,ped_ts])))

    fig, axes = plt.subplots(1, 1)
    
    map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)
    
    plt.scatter(curr_veh_df['x'], curr_veh_df['y'], color="blue", s = 2)
    plt.scatter(curr_ped_df['x'], curr_ped_df['y'], color="red", s=2)
    
    plt.show()

    # Initialize prev_plot_veh & prev_plot_ped as Empty Dataframe
    # Use to store previously plotted data and reuse to plot
    prev_plot_veh = prev_plot_ped = pd.DataFrame()

    for ts in all_timestamp_ms:
        map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)  # Plot Map
        plt.title("Timestamp: " + str(ts))                                       # Give title to Map
        
        # Add vehicles_df row in veh_df if vehicles_df and Current Loop's Timestamp are same
        same_ts_veh_df = curr_veh_df[curr_veh_df['timestamp_ms'] == ts]
        
        # Add pedes_df row in ped_df if pedes_df and Current Loop's Timestamp are same
        same_ts_ped_df = curr_ped_df[curr_ped_df['timestamp_ms'] == ts]
    
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
            
        plt.show()
        
if __name__ == "__main__":
    plot(0, 0)