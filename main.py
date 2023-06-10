import files
import osmtocoordinates as otc
import speed
import distance
import interaction
import plot
import interactions.interact_pair as interact_pair
import allplot 
import pedonroad

#Load Map, Pedestrian & Vehicle Datasets into above variables
map, pedestrian_df, vehicle_df = files.load()
map_coords_df, min_max = otc.getcoords(map, 0, 0)



# Find Speed and Distance covered by Pedestrian & Vehicle 
# Add new column of Speed and Distance covered in Dataframe 
pedestrian_df, vehicle_df = speed.find(pedestrian_df, vehicle_df)
pedestrian_df, vehicle_df = distance.find(pedestrian_df, vehicle_df)

# Find crossing details of Pedestrian
ped_on_road_df = pedonroad.check(map_coords_df, pedestrian_df, vehicle_df)
# call ped_on_road_df

# Find interaction between Pedestrian and Vehicle
#interact_df, ped_on_road_df, poly_coords_dict = interaction.find(vehicle_df, pedestrian_df, map, map_coords_df)

# Plot Vehicle and Pedestrian Coordinates from respective DataFrame 
#ag_plot.visualize(map_coords_df, min_max, pedestrian_df, vehicle_df, map)

#interact_onepair = interact_pair.onepair(interact_df, vehicle_df, pedestrian_df)

# Analysis on Interaction pair(s)
while(True):
    choice = input("Do you want analysis of all interaction pairs or individual pair? \n Y for all interaction pairs or \n N for individual pair\n")
    if choice == "Y":
        #interact_onepair = interact_pair.all(interact_df, vehicle_df, pedestrian_df)
        interact_pair.all(vehicle_df, pedestrian_df, ped_on_road_df)
        break
    elif choice == "N":
        #interact_onepair = interact_pair.individual(interact_df, vehicle_df, pedestrian_df)
        break