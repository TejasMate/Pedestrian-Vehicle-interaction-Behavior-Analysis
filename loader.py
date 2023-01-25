import os
from time import sleep



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
#os.system('cls')

        
trackfiles_path = "recorded_trackfiles/"+mapnames[choice-1]+"/"


os.system('cls')
sleep(1)

trackfiles_path_ids = []
trackfiles = os.listdir(trackfiles_path)
for id in trackfiles:
    id = id.replace(".csv", "")
    id = id.replace("vehicle_tracks_","")
    id = id.replace("pedestrian_tracks_","")
    trackfiles_path_ids.append(id)

trackfiles_path_ids = list(set(trackfiles_path_ids))
trackfiles_path_ids.sort()
print(trackfiles_path_ids)

i = 1
ch = None
while(i):
    ch = input("Enter Recorded Trackfile No.: ")
    if int(ch)>=0 and int(ch)<=len(trackfiles_path_ids):
            i=0
    else:
        print("Enter value in range of 0 to "+ str(len(trackfiles_path_ids)))
        
map_path = "maps/" + mapslist[choice-1]
pedes_ds = "recorded_trackfiles/"+mapnames[choice-1]+"/pedestrian_tracks_"+str(ch)+".csv"
vehicles_ds = "recorded_trackfiles/"+mapnames[choice-1]+"/vehicle_tracks_"+str(ch)+".csv"


def getmappath():
    return map_path

def getpeddspath():
    return pedes_ds

def getvehdspath():
    return vehicles_ds