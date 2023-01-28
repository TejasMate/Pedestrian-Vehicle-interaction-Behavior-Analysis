import matplotlib.pyplot as plt
import pandas as pd
import math

import map_vis_without_lanelet
    
def check(map_path, pedes_df, all_ped_trackids):
    fig, axes = plt.subplots(1, 1)
    map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)
    mappoints = map_vis_without_lanelet.getpoints()
    
    pedstartx = []
    pedstarty = []
    pedstartts = []
    pedendx = []
    pedendy = []
    pedendts = []
    pedx1 = []
    pedy1 = []
    pedx2 = []
    pedy2 = []
    pedx3 = []
    pedy3 = []
    pedx4 = []
    pedy4 = []
    startx = starty = startts = endx =  endy = endts = ''
    
    for p_trackid in all_ped_trackids:
        curr_ped = pedes_df[pedes_df['track_id'] == p_trackid]  
        
        for pedrow in range(0, len(curr_ped)-1):
            outerloop = 0
    
            for maprow in range(0, len(mappoints)-1):
                ped_x = round(curr_ped.iloc[pedrow,4])
                ped_y = round(curr_ped.iloc[pedrow,5])
                map_x = round(mappoints.iloc[maprow,1])
                map_y = round(mappoints.iloc[maprow,2])
      
                if (ped_x == map_x) and (ped_y == map_y):
                    startx = curr_ped.iloc[pedrow,4]
                    starty = curr_ped.iloc[pedrow,5]
                    startts = curr_ped.iloc[pedrow,2]
                    outerloop = 1
                    break
                    
            if outerloop == 1:
                break
                
        for pedrow in range(len(curr_ped)-1, 0, -1):
            outerloop = 0
    
            for maprow in range(len(mappoints)-1, 0, -1):
                ped_x = round(curr_ped.iloc[pedrow,4])
                ped_y = round(curr_ped.iloc[pedrow,5])
                map_x = round(mappoints.iloc[maprow,1])
                map_y = round(mappoints.iloc[maprow,2])
                
                if (ped_x == map_x) and (ped_y == map_y):
                    endx = curr_ped.iloc[pedrow,4]
                    endy = curr_ped.iloc[pedrow,5]
                    endts = curr_ped.iloc[pedrow,2]
                    outerloop = 1
                    break
                    
            if outerloop == 1:
                break
        
        slope = (endy-starty)/(endx-startx)
        rad = math.atan(slope)
        
        x1 = endx-2
        y1 = endy-2
        x4 = startx-2
        y4 = starty-2
        x2 = endx+2
        y2 = endy+2
        x3 = startx+2
        y3 = starty+2
        
        xx1 = x1 * math.cos(rad) + y1 * math.sin(rad)
        yy1 = -x1 * math.sin(rad) + y1 * math.cos(rad)
        xx2 = x2 * math.cos(rad) + y2 * math.sin(rad)
        yy2 = -x2 * math.sin(rad) + y2 * math.cos(rad)
        xx3 = x3 * math.cos(rad) + y3 * math.sin(rad)
        yy3 = -x3 * math.sin(rad) + y3 * math.cos(rad)
        xx4 = x4 * math.cos(rad) + y4 * math.sin(rad)
        yy4 = -x4 * math.sin(rad) + y4 * math.cos(rad)
        
        pedstartx.append(startx)
        pedstarty.append(starty)
        pedstartts.append(startts)
        pedendx.append(endx)
        pedendy.append(endy)
        pedendts.append(endts)
        pedx1.append(xx1)
        pedy1.append(yy1)
        pedx2.append(xx2)
        pedy2.append(yy2)
        pedx3.append(xx3)
        pedy3.append(yy3)
        pedx4.append(xx4)
        pedy4.append(yy4)
     
    ped_on_road_df = pd.DataFrame({'Track ID': all_ped_trackids, 'Crossing starts at X': pedstartx, 'Crossing starts at Y': pedstarty, 'Crossing start at TS': pedstartts,'Crossing ends at X': pedendx, 'Crossing ends at Y': pedendy, 'Crossing ends at TS': pedendts,  'x1': pedx1, 'y1': pedy1, 'x2': pedx2, 'y2': pedy2, 'x3': pedx3, 'y3': pedy3, 'x4': pedx4, 'y4': pedy4})
    ped_on_road_df.to_csv("Pedestrians on road.csv")
    return ped_on_road_df