import  os
import json
import math
from pprint import  pprint
from queue import PriorityQueue
import heapq
import itertools
import time
counter = itertools.count()

class Point:
    def __init__(self,lat,long):
        self.coordinates=(lat,long)
        # self.cluster_id=next(counter)+1
    def print_point(self):
        print("Point:",(self.coordinates))
        # print("Cluster Id:",(self.cluster_id))
        print("Point Type:",self.type)

    def get_lat(self):
        return self.coordinates[0]

    def get_long(self):
        return self.coordinates[1]

def calculate_haversine(point_1,point_2):
    R=6371000
    lat_1=point_1.get_lat()
    long_1=point_1.get_long()
    lat_2=point_2.get_lat()
    long_2=point_2.get_long()
    phi_1=math.radians(lat_1)
    phi_2=math.radians(lat_2)
    delta_phi=math.radians(lat_2-lat_1)
    delta_lamda=math.radians(long_2-long_1)
    a=math.sin(delta_phi/2.0)**2+math.cos(phi_1)*math.cos(phi_2)*math.sin(delta_lamda/2.0)**2
    c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
    distance_in_m=R*c
    distance_in_km=distance_in_m/1000.0
    return distance_in_m


class Cluster:
    def __init__(self):
        self.id=next(counter)+1
        self.point_list=[]

    def addPoint2Cluster(self,point):
        self.point_list.append(point)
        # self.calculateCentroid()

    def calculateCentroid(self):
        lat=0
        long=0
        for point in self.point_list:
            lat+=point.coordinates[0]
            long+=point.coordinates[1]

        self.centroid=Point(float(lat/len(self.point_list)),float(long/len(self.point_list)))

    def getCentroid(self):
        return self.centroid

    def getClusterId(self):
        return self.id

    def getClusterPoints(self):
        return self.point_list
    def nos_points(self):
        return len(self.point_list)

    def print_cluster(self):
        print("Cluster Id:", self.id)
        print("Cluster point number",self.nos_points())
        print("Clustering centroid",self.getCentroid())
        # print("Cluster Id:",(self.cluster_id))


class h_clustering:
    def __init__(self,jsonObject):
        self.cluster_dict=dict()
        self.nos_clusters=0
        self.distance_threshold=100
        for item in jsonObject:
            point_obj=Point(item['coordinates'][0],item['coordinates'][1])
            cluster_obj=Cluster()
            cluster_obj.addPoint2Cluster(point_obj)
            cluster_obj.calculateCentroid()
            self.cluster_dict[cluster_obj.getClusterId()]=cluster_obj
            self.nos_clusters+=1

    def add_cluster(self,cluster_obj):
        self.cluster_dict[cluster_obj.getClusterId()]=cluster_obj
        self.nos_clusters+=1

    def delete_cluster(self,cluster_id):
        if(cluster_id in self.cluster_dict.keys()):
            del self.cluster_dict[cluster_id]
            self.nos_clusters-=1

    def merge_clusters(self,cluster_id_1,cluster_id_2):
        cluster_1=self.cluster_dict[cluster_id_1]
        cluster_2=self.cluster_dict[cluster_id_2]
        combined_cluster=Cluster()
        cluster_1_points=cluster_1.getClusterPoints()
        cluster_2_points=cluster_2.getClusterPoints()
        for point in cluster_1_points:
            combined_cluster.addPoint2Cluster(point)
        for point in cluster_2_points:
            combined_cluster.addPoint2Cluster(point)
        combined_cluster.calculateCentroid()
        self.delete_cluster(cluster_1.getClusterId())
        self.delete_cluster(cluster_2.getClusterId())
        self.add_cluster(combined_cluster)
        return combined_cluster

    def clustering_algorithm(self):
        clustering_heap=[]
        clustering_keys=list(self.cluster_dict.keys())
        for i in range(len(clustering_keys)-1):
            for j in range(i+1,len(clustering_keys)):
                haversine_distance=calculate_haversine(self.cluster_dict[clustering_keys[i]].getCentroid(),self.cluster_dict[clustering_keys[j]].getCentroid())
                # heapq.heappush(heap, entry_1)
                heapq.heappush(clustering_heap,(haversine_distance,clustering_keys[i],clustering_keys[j]))
        combine_flag=True
        print("At the begining:")
        self.print_clustering()
        while(combine_flag):
            popped_item=heapq.heappop(clustering_heap)
            if(popped_item[1] in self.cluster_dict.keys() and popped_item[2] in self.cluster_dict.keys()):
                if(popped_item[0]<=2*self.distance_threshold):
                    cluster_1_id=popped_item[1]
                    cluster_2_id=popped_item[2]
                    merged_cluster=self.merge_clusters(cluster_1_id,cluster_2_id)
                    merged_cluster_id=merged_cluster.getClusterId()
                    self.delete_cluster(cluster_1_id)
                    self.delete_cluster(cluster_2_id)
                    clustering_keys = list(self.cluster_dict.keys())
                    for item in clustering_keys:
                        if(item!=merged_cluster.getClusterId()):
                            haversine_distance=calculate_haversine(self.cluster_dict[merged_cluster_id].getCentroid(),self.cluster_dict[item].getCentroid())
                            heapq.heappush(clustering_heap,(haversine_distance,merged_cluster_id,item))
                            combine_flag=True
                else:
                    combine_flag=False
            else:
                combine_flag=True
        print("At  the end:")
        self.print_clustering()


    def print_clustering(self):
        print("Nos of clusters:",self.nos_clusters)
        # for item in self.cluster_dict.keys():
        #     self.cluster_dict[item].print_cluster()

def clustering_wrapper(jsonFileName):
    with open(jsonDataFile) as fileRead:
        data=json.load(fileRead)
    clustering_obj=h_clustering(data)
    # clustering_obj.print_clustering()
    start_time=time.time()
    clustering_obj.clustering_algorithm()
    print("--- %s seconds ---" % (time.time() - start_time))


def getLatLong(jsonDataFile):
    point_obj=[]
    with open(jsonDataFile) as fileRead:
        data=json.load(fileRead)
    # pprint(data)
    lat_list=[]
    long_list=[]
    for item in data:
        # lat_list.append(item['coordinates'][0])
        # long_list.append(item['coordinates'][1])
        point_obj.append(Point(item['coordinates'][0],item['coordinates'][1],'point'))
    for item in point_obj:
        item.print_point()

    # return lat_list,long_list
    # distance=calculate_haversine(lat_list[0],long_list[0],lat_list[1],long_list[1])
    # print("Coord_1:(%f,%f)" %(lat_list[0],long_list[0]))
    # print("Coord_1:(%f,%f)" % (lat_list[1], long_list[1]))
    # print("Distance is:%f meters" %(distance))
    #


if __name__ == '__main__':
    jsonDataFile = os.path.join('../Data', 'data_1000.json')
    clustering_wrapper(jsonDataFile)

    # getLatLong(jsonDataFile)
    # print("Hello World")
    # heap=[]
    # entry_1=(1,10,10,1)
    # entry_2=(-1,10,10,1)
    # entry_3=(10,10,11,3)
    # entry_4 = (3, 12, 11, -1)
    # heapq.heappush(heap,entry_1)
    # heapq.heappush(heap, entry_2)
    # heapq.heappush(heap, entry_3)
    # heapq.heappush(heap, entry_4)
    # print(type(heapq.heappop(heap)))
    # # print(len(heapq.heappop(heap)))
    # # print(len(heapq.heappop(heap)))
    # # print(len(heapq.heappop(heap)))


