import numpy as np
import matplotlib.pyplot as plt

def plot(single_ped, map_coords_df):

    ped_ts = np.array(single_ped['timestamp_ms'], np.int64)
    all_timestamp_ms = np.sort(np.unique(ped_ts))
        
    # Run Loop one by one for all timestamps
    for ts in all_timestamp_ms:
    
        plt.scatter(map_coords_df['X'], map_coords_df['Y'], s=1.2)
        
        plt.title("Timestamp: " + str(ts))                                       # Give title to Map

        # Add pedes_df row in ped_df if pedes_df and Current Loop's Timestamp are same
        same_ts_ped_df = single_ped[single_ped['timestamp_ms'] == ts]
        
        # Plot Pedestrian coordinate as per current loop's timestamp
        plt.scatter(same_ts_ped_df['x'], same_ts_ped_df['y'], color="red", s=2)
        
        for row in range(0,len(same_ts_ped_df['track_id'])):
            x=same_ts_ped_df.iloc[row,4]                                        # Column 4 -> x
            y=same_ts_ped_df.iloc[row,5]                                        # Column 5 -> y
            track_id= same_ts_ped_df.iloc[row,0]                                # Column 0 -> track_id
            plt.text(x+.1, y+1, track_id , fontsize=7.5)
            
        plt.show()