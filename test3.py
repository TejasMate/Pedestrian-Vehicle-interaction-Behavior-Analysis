import pandas as pd
import math


ID = "003"
ped_onroad_df = pd.read_csv(f"C:/Users/tejas/Downloads/Interaction/Current Code/Generated Files/DR_DEU_Roundabout_OF/{ID}/Pedestrians on road.csv")

pedes_df = pd.read_csv(f"recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_{ID}.csv", engine="pyarrow")

df = pd.DataFrame()
for idx, pedestrian_row in ped_onroad_df.iterrows():
    ped = pedestrian_row['Track ID']
    startts = pedestrian_row['Crossing start at TS']
    endts = pedestrian_row['Crossing ends at TS']
    
    curr_ped = pedes_df[(pedes_df['track_id'] == ped) & (pedes_df['timestamp_ms'] == startts)]
    
    startx= float(curr_ped['x'])
    starty =  float(curr_ped['y'])

    curr_ped = pedes_df[(pedes_df['track_id'] == ped) & (pedes_df['timestamp_ms'] == endts)]
    
    endx = float(curr_ped['x'])
    endy =  float(curr_ped['y'])
    
    lanewidth = math.sqrt((endx - startx)**2 + (endy - starty)**2)
    
    df2 = pd.DataFrame([{'Track ID': ped, 'Crossing start X': startx, 'Crossing start Y': starty, 'Crossing start at TS': startts, 'Crossing ends X': endx, 'Crossing ends Y': endy, 'Crossing ends at TS': endts, 'Lanewidth': lanewidth}])
    df = pd.concat([df, df2]) 

print(df)
dir=f"C:/Users/tejas/Downloads/Interaction/Current Code/Generated Files/DR_DEU_Roundabout_OF/{ID}/Pedestrians on roads.csv"
df.to_csv(dir)
