import matplotlib.pyplot as plt
import pandas as pd

mappoints = pd.read_csv("C:/Users/tejas/Downloads/Interaction/Current Code/Generated Files/DR_USA_Intersection_EP0/mapcoordinates.csv", engine = "pyarrow")

plt.scatter(mappoints['X'], mappoints['Y'], s=0.1)

#plt.plot([1007.39096375, 1007.459, 1008.88629255, 994.00920077, 995.533, 997.74447041, 1007.39096375],[978.55611711, 983.274, 988.36713325, 986.15558139, 981.156, 975.79081343, 978.55611711])  

plt.show()

"""
similar_age_rows = mappoints[mappoints['color'] == "blue"]
plt.scatter(similar_age_rows['X'], similar_age_rows['Y'], marker=marker, c=similar_age_rows['color'])
"""