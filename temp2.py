import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import map_vis_without_lanelet

map_path = "maps/DR_DEU_Roundabout_OF.osm"
pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_000.csv", engine="pyarrow")
vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_000.csv", engine="pyarrow")     

ped = "P1"
veh = 3

fig, axes = plt.subplots(1, 1)

veh_ts = vehicles_df.loc[(vehicles_df['track_id'] == veh), 'timestamp_ms']
ped_ts = pedes_df.loc[(pedes_df['track_id'] == ped), 'timestamp_ms']

merges_ts = pd.concat([veh_ts, ped_ts], axis=0)
merges_ts = merges_ts.to_numpy()
all_ts = np.sort(np.unique(merges_ts))

prev_plot_veh = prev_plot_ped = pd.DataFrame()

for ts in all_ts:
    map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)
    
    same_ts_veh_df = vehicles_df[(vehicles_df['timestamp_ms'] == ts) & (vehicles_df['track_id'] == veh)]
    same_ts_ped_df = pedes_df[(pedes_df['timestamp_ms'] == ts) & (pedes_df['track_id'] == ped)]

    prev_plot_veh = pd.concat([prev_plot_veh, same_ts_veh_df], ignore_index = True)    
    prev_plot_ped = pd.concat([prev_plot_ped, same_ts_ped_df], ignore_index = True)
    
    plt.scatter(prev_plot_veh['x'], prev_plot_veh['y'], color="lightblue", s=prev_plot_veh['width'])
    plt.scatter(prev_plot_ped['x'], prev_plot_ped['y'], color="orange", s=2)
    plt.scatter(same_ts_veh_df['x'], same_ts_veh_df['y'], color="blue")
    plt.scatter(same_ts_ped_df['x'], same_ts_ped_df['y'], color="red")
    
    plt.plot([1007.39096375, 1007.459, 1008.88629255, 994.00920077, 995.533, 997.74447041, 1007.39096375],[978.55611711, 983.274, 988.36713325, 986.15558139, 981.156, 975.79081343, 978.55611711])  
    
    plt.title("Timestamp: " + str(ts))                                       
    plt.show()