import pandas as pd
import numpy as np

mappoints = pd.read_csv("mappoints.csv")

local_mappoints = np.array(mappoints[['x' ,'y']])

print(local_mappoints)

def solve(pts, pt):
   x, y = pt
   idx = -1
   smallest = float("inf")
   for p in pts:
       ptsx = float("{:.3f}".format(p[0]))
       ptsy = float("{:.3f}".format(p[1]))
       x    = float("{:.3f}".format(x))
       y    = float("{:.3f}".format(y))
       

       xcond = ycond = False
       
       for count in range(0, 1000):
           if ptsx == x:
              xcond = True
              break
           else:
              x+=0.001
              
       for count in range(0, 1000):
           if ptsy == y:
              ycond = True
              break
           else:
              y+=0.001
              
       if xcond or ycond:
          dist = abs(x - p[0]) + abs(y - p[1])
          if dist < smallest:
             idx = pts.index(p)
             smallest = dist
          elif dist == smallest:
             if pts.index(p) < idx:
                idx = pts.index(p)
                smallest = dist
       return idx

pts = local_mappoints.tolist()
pt = [1005.630, 984.816]
print(type(pts[0]))
print(solve(pts, pt))