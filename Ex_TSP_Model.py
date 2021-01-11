import random
import math

class Node:
    def __init__(self, id, tp, dem, xx, yy):
        self.id = id
        self.type = tp
        self.demand = dem
        self.x = xx
        self.y = yy
        self.isRouted = False

class Route:
    def __init__(self, dp, cap):
        self.sequenceOfNodes = []
        self.sequenceOfNodes.append(dp)
        self.sequenceOfNodes.append(dp)
        self.cost = 0
        self.capacity = cap
        self.load = 0


class Model:
# instance variables
    def __init__(self):
        #allNodes
        self.all_nodes = []
        #customers
        self.service_locations = []
        #matrix
        self.dist_matrix = []
        self.capacity = -1

    def BuildModel(self):
        random.seed(5)
        depot = Node(0, 50, 50)
        self.all_nodes.append(depot)
        self.capacity = 3000
        totalCustomers = 200
        for i in range (0, totalCustomers):
            id = i + 1
            tp = random.randint(1, 3)
            dem = random.randint(1, 5) * 100
            xx = random.randint(0, 100)
            yy = random.randint(0, 100)
            #cust
            serv_node = Node(id, tp, dem, xx, yy)
            self.all_nodes.append(serv_node)
            self.service_locations.append(serv_node)

        rows = len(self.all_nodes)
        self.dist_matrix = [[0.0 for j in range(rows)] for k in range(rows)]

        for i in range(0, len(self.all_nodes)):
            for j in range(0, len(self.all_nodes)):
                source = self.all_nodes[i]
                target = self.all_nodes[j]
                dx_2 = (source.x - target.x) ** 2
                dy_2 = (source.y - target.y) ** 2
                dist = round(math.sqrt(dx_2 + dy_2))
                self.dist_matrix[i][j] = dist
