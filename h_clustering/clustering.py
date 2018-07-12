import  os
import json
import math
from pprint import  pprint
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
def calculate_haversine(lat_1,long_1,lat_2,long_2):
    R=6371000
    phi_1=math.radians(lat_1)
    phi_2=math.radians(lat_2)
    delta_phi=math.radians(lat_2-lat_1)
    delta_lamda=math.radians(long_2-long_1)
    a=math.sin(delta_phi/2.0)**2+math.cos(phi_1)*math.cos(phi_2)*math.sin(delta_lamda/2.0)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    distance_in_m=R*c
    distance_in_km=distance_in_m/1000.0
    return distance_in_m
def getLatLong(jsonDataFile):
    with open(jsonDataFile) as fileRead:
        data=json.load(fileRead)
    # pprint(data)
    lat_list=[]
    long_list=[]
    for item in data:
        lat_list.append(item['coordinates'][0])
        long_list.append(item['coordinates'][1])
    # return lat_list,long_list
    # distance=calculate_haversine(lat_list[0],long_list[0],lat_list[1],long_list[1])
    # print("Coord_1:(%f,%f)" %(lat_list[0],long_list[0]))
    # print("Coord_1:(%f,%f)" % (lat_list[1], long_list[1]))
    # print("Distance is:%f meters" %(distance))


if __name__ == '__main__':
    jsonDataFile = os.path.join('../Data', 'data_1000.json')
    getLatLong(jsonDataFile)
