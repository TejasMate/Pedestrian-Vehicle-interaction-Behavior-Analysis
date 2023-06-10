import matplotlib.pyplot as plt
import xml.etree.ElementTree as xml
import pyproj
import math
import pandas as pd
import files
import os
import numpy as np
import dict_utils

def create_line(x, y):
    plt.scatter(x, y, color="black", s=1)
    plt.show()
    pass

def get_line_coordinates(x, y):
    coordinates = []
    for i in range(len(x)-1):
        x_values = np.linspace(x[i], x[i+1], num=100)
        y_values = np.linspace(y[i], y[i+1], num=100)
        points = np.column_stack((x_values, y_values))
        coordinates.extend(points)
    return coordinates

class Point:
    def __init__(self):
        self.x = None
        self.y = None

class LL2XYProjector:
    def __init__(self, lat_origin, lon_origin):
        self.lat_origin = lat_origin
        self.lon_origin = lon_origin
        self.zone = math.floor((lon_origin + 180.) / 6) + 1  # works for most tiles, and for all in the dataset
        self.p = pyproj.Proj(proj='utm', ellps='WGS84', zone=self.zone, datum='WGS84')
        [self.x_origin, self.y_origin] = self.p(lon_origin, lat_origin)


    def latlon2xy(self, lat, lon):
        [x, y] = self.p(lon, lat)
        return [x - self.x_origin, y - self.y_origin]

def get_type(element):
    for tag in element.findall("tag"):
        if tag.get("k") == "type":
            return tag.get("v")
    return None

def get_subtype(element):
    for tag in element.findall("tag"):
        if tag.get("k") == "subtype":
            return tag.get("v")
    return None

def get_x_y_lists(element, point_dict):
    x_list = y_list = list()
    for nd in element.findall("nd"):
        pt_id = int(nd.get("ref"))
        point = point_dict[pt_id]
        x_list.append(point.x)
        y_list.append(point.y)
    return x_list, y_list

def getcoords(filename, lat_origin, lon_origin):
    
    if os.path.exists(f"{files.MAP_DATA}/mapcoordinates.csv"):
        mapcoordinates = pd.read_csv(f"{files.MAP_DATA}/mapcoordinates.csv")
        min_max = {"min_x": mapcoordinates['X'].min(), "min_y": mapcoordinates['Y'].min(), "max_x": mapcoordinates['X'].max(), "max_y": mapcoordinates['Y'].max()}
        return mapcoordinates, min_max
    
    e = xml.parse(filename).getroot()
    projector = LL2XYProjector(lat_origin, lon_origin)

    point_dict = dict()
    for node in e.findall("node"):
        point = Point()
        point.x, point.y = projector.latlon2xy(float(node.get('lat')), float(node.get('lon')))
        point_dict[int(node.get('id'))] = point

    unknown_linestring_types = list()
    
    curbstone_coordinates = line_thin_dashed_coordinates = line_thin_other_coordinates = line_thick_dashed_coordinates = line_thick_other_coordinates = pedestrian_marking_coordinates = bike_marking_coordinates = stop_line_coordinates = virtual_coordinates = road_border_coordinates = guard_rail_coordinates = list()
    mapcoordinates = pd.DataFrame()
    for way in e.findall('way'):
        way_type = get_type(way)
        
        if way_type is None:
            raise RuntimeError("Linestring type must be specified")
        elif way_type == "curbstone":
            type_dict = dict(color="black", linewidth=1.5, zorder=10)
            x_list, y_list = get_x_y_lists(way, point_dict)
            curbstone_coordinates = curbstone_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in curbstone_coordinates], [round(coord[1], 3) for coord in curbstone_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = np.nan * len(x_line)
            df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33])  
        """
        elif way_type == "line_thin":
            way_subtype = get_subtype(way)
            if way_subtype == "dashed":
                type_dict = dict(color="white", linewidth=1, zorder=10, dashes=[10, 10])
                x_list, y_list = get_x_y_lists(way, point_dict)
                line_thin_dashed_coordinates = line_thin_dashed_coordinates + get_line_coordinates(x_list, y_list)
                x_line, y_line = [round(coord[0], 3) for coord in line_thin_dashed_coordinates], [round(coord[1], 3) for coord in line_thin_dashed_coordinates]
                color_list = [type_dict['color']] * len(x_line)
                linewidth_list = [type_dict['linewidth']] * len(x_line)
                zorder_list = [type_dict['zorder']] * len(x_line)
                dashes = [type_dict['dashes']] * len(x_line)
                df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
                mapcoordinates = pd.concat([mapcoordinates, df33]) 

            else:
                type_dict = dict(color="white", linewidth=1, zorder=10)
                x_list, y_list = get_x_y_lists(way, point_dict)
                line_thin_other_coordinates = line_thin_other_coordinates + get_line_coordinates(x_list, y_list)
                x_line, y_line = [round(coord[0], 3) for coord in line_thin_other_coordinates], [round(coord[1], 3) for coord in line_thin_other_coordinates]
                color_list = [type_dict['color']] * len(x_line)
                linewidth_list = [type_dict['linewidth']] * len(x_line)
                zorder_list = [type_dict['zorder']] * len(x_line)
                dashes = np.nan * len(x_line)
                df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
                mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "line_thick":
            way_subtype = get_subtype(way)
            if way_subtype == "dashed":
                type_dict = dict(color="white", linewidth=2, zorder=10, dashes=[10, 10])
                x_list, y_list = get_x_y_lists(way, point_dict)
                line_thick_dashed_coordinates = line_thick_dashed_coordinates + get_line_coordinates(x_list, y_list)
                x_line, y_line = [round(coord[0], 3) for coord in line_thick_dashed_coordinates], [round(coord[1], 3) for coord in line_thick_dashed_coordinates]
                color_list = [type_dict['color']] * len(x_line)
                linewidth_list = [type_dict['linewidth']] * len(x_line)
                zorder_list = [type_dict['zorder']] * len(x_line)
                dashes = [type_dict['dashes']] * len(x_line)
                df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
                mapcoordinates = pd.concat([mapcoordinates, df33]) 

            else:
                type_dict = dict(color="white", linewidth=2, zorder=10)
                x_list, y_list = get_x_y_lists(way, point_dict)
                line_thick_other_coordinates = line_thick_other_coordinates + get_line_coordinates(x_list, y_list)
                x_line, y_line = [round(coord[0], 3) for coord in line_thick_other_coordinates], [round(coord[1], 3) for coord in line_thick_other_coordinates]
                color_list = [type_dict['color']] * len(x_line)
                linewidth_list = [type_dict['linewidth']] * len(x_line)
                zorder_list = [type_dict['zorder']] * len(x_line)
                dashes = np.nan * len(x_line)
                df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
                mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "pedestrian_marking":
            type_dict = dict(color="white", linewidth=1, zorder=10, dashes=[5, 10])
            x_list, y_list = get_x_y_lists(way, point_dict)
            pedestrian_marking_coordinates = pedestrian_marking_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in pedestrian_marking_coordinates], [round(coord[1], 3) for coord in pedestrian_marking_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = [type_dict['dashes']] * len(x_line)
            df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "bike_marking":
            type_dict = dict(color="white", linewidth=1, zorder=10, dashes=[5, 10])
            x_list, y_list = get_x_y_lists(way, point_dict)
            bike_marking_coordinates = bike_marking_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in bike_marking_coordinates], [round(coord[1], 3) for coord in bike_marking_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = [type_dict['dashes']] * len(x_line)
            df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "stop_line":
            type_dict = dict(color="white", linewidth=3, zorder=10)
            x_list, y_list = get_x_y_lists(way, point_dict)
            stop_line_coordinates = stop_line_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in stop_line_coordinates], [round(coord[1], 3) for coord in stop_line_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = np.nan * len(x_line)
            df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "virtual":
            type_dict = dict(color="blue", linewidth=1.2, zorder=10, dashes=[2, 5])
            x_list, y_list = get_x_y_lists(way, point_dict)
            virtual_coordinates = virtual_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in virtual_coordinates], [round(coord[1], 3) for coord in virtual_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = [type_dict['dashes']] * len(x_line)
            df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "road_border":
            type_dict = dict(color="black", linewidth=1.5, zorder=10)
            x_list, y_list = get_x_y_lists(way, point_dict)
            road_border_coordinates = road_border_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in road_border_coordinates], [round(coord[1], 3) for coord in road_border_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = np.nan * len(x_line)
            df33 = pd.DataFrame({'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "guard_rail":
            type_dict = dict(color="black", linewidth=1, zorder=10)
            x_list, y_list = get_x_y_lists(way, point_dict)
            guard_rail_coordinates = guard_rail_coordinates + get_line_coordinates(x_list, y_list)
            x_line, y_line = [round(coord[0], 3) for coord in guard_rail_coordinates], [round(coord[1], 3) for coord in guard_rail_coordinates]
            color_list = [type_dict['color']] * len(x_line)
            linewidth_list = [type_dict['linewidth']] * len(x_line)
            zorder_list = [type_dict['zorder']] * len(x_line)
            dashes = np.nan * len(x_line)
            way_types = way_type * len(x_line)
            df33 = pd.DataFrame({'way_type': way_types, 'X': x_line, 'Y': y_line, 'color': color_list,  'linewidth': linewidth_list, 'zorder': zorder_list, 'dashes': dashes})
            mapcoordinates = pd.concat([mapcoordinates, df33]) 

        elif way_type == "traffic_sign":
            continue
        
        else:
            if way_type not in unknown_linestring_types:
                unknown_linestring_types.append(way_type)
            continue
        """
    
    mapcoordinates['dashes'] = mapcoordinates['dashes'].apply(lambda x: tuple([x]) if isinstance(x, float) else tuple(x))
    mapcoordinates = mapcoordinates.drop_duplicates()
    mapcoordinates = mapcoordinates.sort_values('X')
    mapcoordinates.to_csv(f"{files.MAP_DATA}/mapcoordinates.csv", index = False)
    min_max = {"min_x": mapcoordinates['X'].min(), "min_y": mapcoordinates['Y'].min(), "max_x": mapcoordinates['X'].max(), "max_y": mapcoordinates['Y'].max()}

    return mapcoordinates, min_max