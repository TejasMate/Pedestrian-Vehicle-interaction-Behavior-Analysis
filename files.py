import os
import pandas as pd

MAP_DATA = TRACKFILE_DATA = ''

def askmap():
    mapslist = [m for m in os.listdir('maps/') if any("pedestrian" in f for f in os.listdir(f"recorded_trackfiles/{m.replace('.osm', '')}/"))]
    mapnames = []
    global map_name
    
    print("Available Maps are")
    for index_no, map in enumerate(mapslist, start=1):
        map_name = map.replace(".osm", "")
        mapnames.append(map_name)
        map_name = map_name.replace("_", " ").replace("DR", "")
        print(f"{index_no}. {map_name}")

    while True:
        choice = int(input(f"Enter Map no. (1 to {len(mapslist)}): "))
        if 1 <= choice <= len(mapslist):
            map_name = mapnames[choice-1]
            map_file = mapslist[choice-1]
            break
        else:
            print(f"Enter value in range of 1 to {len(mapslist)}")
            
    print(map_name)
    return map_file


def asktrackfile():
    trackfiles_path = f"recorded_trackfiles/{map_name}/"

    trackfiles_in_path = {id.replace(".csv", "").replace("vehicle_tracks_", "").replace("pedestrian_tracks_", "") for id in os.listdir(trackfiles_path)}
    trackfiles_in_path = sorted(list(trackfiles_in_path))
    print(trackfiles_in_path)

    while True:
        choice = input(f"Enter Recorded Trackfile No. (0 to {len(trackfiles_in_path)}): ")
        if choice.isdigit() and 0 <= int(choice) <= len(trackfiles_in_path):
            break
        else:
            print(f"Enter value in range of 0 to {len(trackfiles_in_path)}")

    return choice


def dataframe_optimise(*dfs):
    optimized_dfs = []
    for df in dfs:
        df.reset_index(drop=True, inplace=True)
        optimized_dfs.append(df)
    return optimized_dfs

def load():
    map_path = "maps/" + askmap()
    recordfile_no = asktrackfile()

    global MAP_DATA, TRACKFILE_DATA
    MAP_DATA = f"Generated Files/{map_name}"
    TRACKFILE_DATA = f"Generated Files/{map_name}/{recordfile_no}"
    if not os.path.exists(MAP_DATA):
        os.makedirs(MAP_DATA)
        os.makedirs(TRACKFILE_DATA)
    elif not os.path.exists(TRACKFILE_DATA):
        os.makedirs(TRACKFILE_DATA)
        
    
    ped_ds_path = f"recorded_trackfiles/{map_name}/pedestrian_tracks_{recordfile_no}.csv"
    veh_ds_path = f"recorded_trackfiles/{map_name}/vehicle_tracks_{recordfile_no}.csv"
    
    # Converting Datasets into Dataframe
    pedestrian_df = pd.read_csv(ped_ds_path, engine="pyarrow")
    vehicles_df = pd.read_csv(veh_ds_path, engine="pyarrow")
    pedestrian_df, vehicles_df = dataframe_optimise(pedestrian_df, vehicles_df)
    
    return map_path, pedestrian_df, vehicles_df

    """    
    map_path = 'maps/DR_DEU_Roundabout_OF.osm'
    # Converting Datasets into Dataframe
    pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_001.csv", engine="pyarrow")
    vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_001.csv", engine="pyarrow")
    return map_path, pedes_df, vehicles_df
    """

