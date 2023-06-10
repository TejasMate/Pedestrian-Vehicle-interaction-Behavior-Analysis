"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
       # Plotting Vehicle, Pedestrian Data on Map
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import drawpolygon
import osmtocoordinates as osmtocoords

def set_visible_area(min_max, axes):

    axes.set_aspect('equal', adjustable='box')
    axes.patch.set_facecolor('lightgrey')
    axes.set_xlim([min_max["min_x"] - 10, min_max["max_x"] + 10])
    axes.set_ylim([min_max["min_y"] - 10, min_max["max_y"] + 10])


def visualize(map_coords_df, min_max, pedes_df, vehicles_df, map):
    
    # to subplot only one visual
    fig, axes = plt.subplots(1, 1)
    set_visible_area(min_max, axes)

    # Initialize prev_plot_veh & prev_plot_ped as Empty Dataframe
    # Use to store previously plotted data and reuse to plot
    prev_plot_veh = pd.DataFrame()
    prev_plot_ped = pd.DataFrame()
    
    # Create Array of vehicles & pedestrian timestamp
    veh_ts = np.array(vehicles_df['timestamp_ms'], np.int64)
    ped_ts = np.array(pedes_df['timestamp_ms'], np.int64)
    
    all_timestamp_ms = np.sort(np.unique(np.concatenate((veh_ts,ped_ts))))
    all_timestamp_ms = all_timestamp_ms[all_timestamp_ms >= 16000]
    
    
    
    #all_way_types = np.unique(np.array(map_coords_df['Way type']))
    #way_type_grp = map_coords_df.groupby('Way type')

    
    # Run Loop one by one for all timestamps
    for ts in all_timestamp_ms:
        plt.title("Timestamp: " + str(ts))    
        
        osmtocoords.visualize(map, 0, 0)
        
        """
        for wt in all_way_types:          
            curr_way_type_grp = way_type_grp.get_group(wt)
            
            first_row_of_grp = curr_way_type_grp.iloc[0] 
            linewid = float(first_row_of_grp['linewidth'])
            col = first_row_of_grp['color']
            zord = int(first_row_of_grp['zorder'])
            dash = first_row_of_grp['dashes']
            

            if type(dash) == list:
                type_dict = dict(color=col, linewidth=linewid, zorder=zord, dashes= dash)
                plt.plot(curr_way_type_grp['x'], curr_way_type_grp['y'], **type_dict)
            elif type(dash) != list:
                type_dict = dict(color=col, zorder=zord, s = 1.5)
                plt.scatter(curr_way_type_grp['x'], curr_way_type_grp['y'], **type_dict)

            #else:
            #    plt.plot(curr_way_type_grp['x'], curr_way_type_grp['y'], color=col, linewidth=linewid, zorder=zord)


            #if wt == "curbstone"
            


        #plt.scatter(map_coords_df['x'], map_coords_df['y'], color="black", linewidth=1.5, zorder=10, s = 1)
        """
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
            
            """
            coords = drawpolygon.get(track_id)
            xs, ys = zip(*coords)
            plt.plot(xs,ys)      
            """

            # Plot Pedestrian interaction with vehicles on X Axis Label
            #plotinter = interaction_in_short[interaction_in_short['Pedestrian TrackID'] == track_id]
            #string = str(list(plotinter['Vehicle TrackID']))
            #plt.xlabel(str(track_id) + " can collide with vehicles: " + string)     
            
        
        plt.show()
        return