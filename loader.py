import os
from time import sleep

def askmap():        
    mapslist = os.listdir("maps/")
    mapnames = []
    
    temp1 = mapslist.copy()
    for J in temp1:
        #print(J)
        trackfiles_path = "recorded_trackfiles/"+J+"/"
        trackfiles_path = trackfiles_path.replace(".osm","")
        trackfiles = os.listdir(trackfiles_path)
    
        count = 0
        
        for y in trackfiles:
            if "pedestrian" in y:
                count+=1
                break;
    
        if count == 0:
            mapslist.remove(J)
    
    os.system('cls')
    sleep(1)
    
    index_no = 1
    
    print("Available Maps are")
    for map in mapslist:
        map = map.replace(".osm","")
        mapnames.append(map)
        map = map.replace("_"," ")
        map = map.replace("DR","")
        print(str(index_no)+". "+map)
        index_no+=1
        
    i = 1
    while(i):
        choice = int(input("Enter Map no.: "))
        if choice>=1 and choice<=len(mapslist):
                i=0
        else:
            print("Enter value in range of 1 to "+ str(len(mapslist)))
    
    global map_name
    map_name = mapnames[choice-1]
    global map_file
    map_file = mapslist[choice-1]

def asktrackfile():
    trackfiles_path = "recorded_trackfiles/"+map_name+"/"
    
    trackfiles_in_path = []
    trackfiles = os.listdir(trackfiles_path)
    for id in trackfiles:
        id = id.replace(".csv", "")
        id = id.replace("vehicle_tracks_","")
        id = id.replace("pedestrian_tracks_","")
        trackfiles_in_path.append(id)
        
    os.system('cls')
    sleep(1)
    
    trackfiles_in_path = list(set(trackfiles_in_path))
    trackfiles_in_path.sort()
    print(trackfiles_in_path)
    
    i = 1
    global ch
    ch = None
    while(i):
        ch = input("Enter Recorded Trackfile No.: ")
        if int(ch)>=0 and int(ch)<=len(trackfiles_in_path):
                i=0
        else:
            print("Enter value in range of 0 to "+ str(len(trackfiles_in_path)))

def getpath():
    askmap()
    asktrackfile()
    map_path = "maps/" + map_file
    ped_ds_path = "recorded_trackfiles/"+map_name+"/pedestrian_tracks_"+str(ch)+".csv"
    veh_ds_path = "recorded_trackfiles/"+map_name+"/vehicle_tracks_"+str(ch)+".csv"
    return map_path, ped_ds_path, veh_ds_path