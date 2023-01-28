# Readymade modules 
import pandas as pd
import numpy as np

# Custom made modules
import loader
import plot
import vehicle_speed as spd
import pedonroad
import interaction

#map_path = 'maps/DR_DEU_Roundabout_OF.osm'
#pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_000.csv")
#vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_000.csv")

# Path of Map, Pedestrian & Vehicle Datasets
map_path, ped_df_path, veh_df_path = loader.getpath()

# Converting Datasets into Dataframe
pedes_df = pd.read_csv(ped_df_path)
vehicles_df = pd.read_csv(veh_df_path)

all_veh_trackids = np.unique(vehicles_df['track_id'].to_numpy())
all_ped_trackids = np.unique(pedes_df['track_id'].to_numpy())

vehicles_df['speed'] = ''
vehicles_df, vehicles_avg_speed = spd.speed(vehicles_df, all_veh_trackids)

ped_on_road_df = pedonroad.check(map_path, pedes_df, all_ped_trackids)

interact_df = interaction.interact(vehicles_df, pedes_df, all_veh_trackids, all_ped_trackids, ped_on_road_df)

plot.one(vehicles_df, pedes_df, interact_df, map_path)




#print("1. Plot only current trajectory without any Past/Future trajectories of every Pedestrian & Vehicle")
#print("2. Plot current trajectory with Previous 10 and Next 10 trajectories of every Pedestrian & Vehicle") 


# Plot only current trajectory without any Past/Future trajectories of every Pedestrian & Vehicle
# plot.one(vehicles_df, pedes_df, interaction_in_short, map_path)

# Plot current trajectory with Previous 10 and Next 10 trajectories of every Pedestrian & Vehicle
#plot.two(vehicles_df, pedes_df, interact_df, map_path)

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



