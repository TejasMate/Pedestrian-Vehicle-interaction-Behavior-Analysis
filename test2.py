import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.patches import Polygon

# Use map_vis_without_Lanelet library to visual Map
import map_vis_without_lanelet

map_path = 'maps/DR_USA_Intersection_EP0.osm'
# Converting Datasets into Dataframe
pedes_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/pedestrian_tracks_001.csv", engine="pyarrow")
vehicles_df = pd.read_csv("recorded_trackfiles/DR_DEU_Roundabout_OF/vehicle_tracks_001.csv", engine="pyarrow")

fig, axes = plt.subplots(1, 1)
map_vis_without_lanelet.draw_map_without_lanelet(map_path, axes, 0, 0)  # Plot Map

coordinates1 = [(994, 994), (994.5, 997), (994.5, 1000), (1005, 1000),  (1005, 997), (1006, 995), (1007, 994)]
coordinates2 = [(1021.8,972.5), (1021.8,975), (1022,978), (1029,977.5),  (1029, 974.5), (1029,971.8)]
coordinates3 = [(983,982), (983,984), (983.2,990.5), (989,990.5),  (989, 987), (989,981.5)]
coordinates4 = [(1008.2,980.5), (1008.5,985), (1008.9,993), (1015.9,993),  (1015.5, 986), (1015.3,980.0)]
coordinates5 = [(1040.8,970.2), (1040.8,972), (1041,975), (1049.8,974.8),  (1048,972.371), (1048,970)]


polygon = Polygon(coordinates1, closed=True, edgecolor='green', facecolor='none', zorder=10, linewidth=2)
axes.add_patch(polygon)

polygon = Polygon(coordinates2, closed=True, edgecolor='yellow', facecolor='none', zorder=10, linewidth=2)
axes.add_patch(polygon)

polygon = Polygon(coordinates3, closed=True, edgecolor='red', facecolor='none', zorder=10, linewidth=2)
axes.add_patch(polygon)

polygon = Polygon(coordinates4, closed=True, edgecolor='purple', facecolor='none', zorder=10, linewidth=2)
axes.add_patch(polygon)

polygon = Polygon(coordinates5, closed=True, edgecolor='pink', facecolor='none', zorder=10, linewidth=2)
axes.add_patch(polygon)

label = 'Interaction\n Zone 1'
axes.text(986, 975, label, ha='center', va='center', fontsize=6.5, fontweight='bold', zorder=10)

label = 'Interaction\n Zone 2'
axes.text(1000, 1005, label, ha='center', va='center', fontsize=6.5, fontweight='bold', zorder=10)

label = 'Interaction\n Zone 3'
axes.text(1026, 988, label, ha='center', va='center', fontsize=6.5, fontweight='bold', zorder=10)

label = 'Interaction\n Zone 4'
axes.text(1026, 967, label, ha='center', va='center', fontsize=6.5, fontweight='bold', zorder=10)

label = 'Interaction\n Zone 5'
axes.text(1045, 965, label, ha='center', va='center', fontsize=6.5, fontweight='bold', zorder=10)


plt.show()