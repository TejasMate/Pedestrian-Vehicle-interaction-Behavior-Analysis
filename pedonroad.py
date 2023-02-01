import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np

import map_vis_without_lanelet
    
"""
def pedroadarea(all_ped_trackids, ped_on_road_df, mappoints):
    pedroadarea = pd.DataFrame()
    local_mappoints = np.array(mappoints[['x' ,'y']])
    
    hor_mappoints = mappoints.sort_values(by=['x', 'y'])   
    ver_mappoints = mappoints.sort_values(by=['y', 'x'])

    for row in ped_on_road_df:
        start_x = ped_on_road_df.iloc[row,1]
        start_y = ped_on_road_df.iloc[row,2]
        end_x = ped_on_road_df.iloc[row,4]
        end_y = ped_on_road_df.iloc[row,5]

        x_gap = abs(start_x - end_x)
        y_gap = abs(start_y - end_y)

        if x_gap > y_gap:
            print("pedestrian walking in horizontal direction")
            print("coverage increased by x sides") #x firsy
        elif y_gap> x_gap:
            index = df[df[‘Name’]==’Donna’].index.values)
            print("vertical walking")
            print("coverage increased by y sides")  #y first
        else:
            print("Linear walking")
        

    
    print(local_mappoints)
    
    for ped in all_ped_trackids:
        start_points = np.array([[ped_on_road_df.iloc[row,1],ped_on_road_df.iloc[row,2]]])
        start_local_mappoints = np.setdiff1d(local_mappoints, start_points)
        
        i = 1
        first = 0      

        while(i):
            
            dist = []
            c = 0
            least_distance = 0
            for i in range(0, len(start_local_mappoints)):
                xa = int(line_points[i][0])
                ya = int(pt[0])
                xb = int(line_points[i][1])
                yb = int(pt[1])
                # Euclidean distance formula
                distance = math.sqrt(((xa – ya)**2) + ((xb – yb)**2))
                dist.append(distance)
                # Finding the least distance value
                if distance <= least_distance:
                    least_distance = distance
            
            # Finding the points with least distance
            c_list = list()
            for i in range(len(dist)):
                if dist[i] == least_distance:
                    c_list.append(line_points[i])

print("Points which are closer to the point P : ", tuple(c_list))
                
    """        
        
    """
    for row in range(0,len(ped_on_road_df)):
        
        
        
        startts = ped_on_road_df.iloc[row,3]
        endts = ped_on_road_df.iloc[row,6]
        
        start_x = ped_on_road_df.iloc[row,1]
        start_y = ped_on_road_df.iloc[row,2]
        end_x = ped_on_road_df.iloc[row,4]
        end_y = ped_on_road_df.iloc[row,5]

        start_line = []
        
        
        suppose_lr_x = startts+1
        suppose_lr_y = 
        
        condition = 1
        while(condition):
            
            condition = 0
    """
        


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
                map_x = round(mappoints.iloc[maprow,0])
                map_y = round(mappoints.iloc[maprow,1])
      
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
                map_x = round(mappoints.iloc[maprow,0])
                map_y = round(mappoints.iloc[maprow,1])
                
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
    
    #pedroadarea(all_ped_trackids, ped_on_road_df, mappoints)
    
    
    return ped_on_road_df