import random
import math


class Model:
    # instance variables
    def __init__(self):
        self.all_nodes = []
        self.service_locations = []
        self.matrix = []
        self.Trucks=[]

    def BuildModel(self):

        self.all_nodes = []
        self.service_locations = []
        depot = Node(0, 0, 0, 50, 50)
        self.all_nodes.append(depot)
        random.seed(1)
        for i in range(0, 200):
            id = i + 1
            tp = random.randint(1, 3)
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            serv_node = Node(id, tp, dem, xx, yy)
            self.all_nodes.append(serv_node)
            self.service_locations.append(serv_node)

        self.matrix = [[0.0 for j in range(0, len(self.all_nodes))] for k in range(0, len(self.all_nodes))]
        for i in range(0, len(self.all_nodes)):
            for j in range(0, len(self.all_nodes)):
                source = self.all_nodes[i]
                target = self.all_nodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                self.matrix[i][j] = dist
        for i in range(0, 25):
            serv_truck = Truck()
            self.Trucks.append(serv_truck)



class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy

class Truck:
    def __init__(self):
        self.cost = 0.0
        self.sequenceOfNodes = []
        self.dem=0
