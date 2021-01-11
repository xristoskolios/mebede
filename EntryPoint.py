from TSP_Model import Model
from SolutionDrawer import *

class Solution:
    def __init__(self):
        self.cost = 0.0
        self.sequenceOfTrucks = []




def ApplyNearestNeighborMethod(depot, service_locations, sol, matrix,Trucks):

    for l in range(0,len(Trucks)):
            Trucks[l].sequenceOfNodes.append(depot)
    for i in range (0, len(service_locations)):
         for l in range(0,len(Trucks)):
                indexOfTheNextService_locations = -1
                minimumInsertionCost = 100000
                lastIndexInSolution = len(Trucks[l].sequenceOfNodes) - 1
                lastNodeInTheCurrentSequence = Trucks[l].sequenceOfNodes[lastIndexInSolution]

                for j in range (0, len(service_locations)):
                    candidate = service_locations[j]
                    if candidate.demand == 0:
                        continue
                    trialCost = matrix[lastNodeInTheCurrentSequence.id][candidate.id]/35
                    if candidate.type==1:
                        trialCost += 5/60
                    elif candidate.type==2:
                        trialCost += 15/60
                    else:
                        trialCost += 25/60
                    if ((trialCost < minimumInsertionCost) & (Trucks[l].dem + candidate.demand <= 3000)) :
                        indexOfTheNextService_locations = j
                        minimumInsertionCost = trialCost

                insertedService_locations = service_locations[indexOfTheNextService_locations]
                if insertedService_locations.demand!=0:
                    Trucks[l].sequenceOfNodes.append(insertedService_locations)
                    Trucks[l].cost += minimumInsertionCost
                    Trucks[l].dem += insertedService_locations.demand
                    insertedService_locations.demand=0

    for l in range(0,len(Trucks)):
        Trucks[l].sequenceOfNodes.append(depot)
        sol.sequenceOfTrucks.append(Trucks[l])
    cost=0
    for i in range (0, len(Trucks)):
        if Trucks[i].cost >cost:
            cost=Trucks[i].cost
    sol.cost=cost


def MinimumInsertions(depot, service_locations, sol, matrix,Trucks):
    q=0
    for l in range(0,len(Trucks)):
        Trucks[l].sequenceOfNodes.append(depot)
        Trucks[l].sequenceOfNodes.append(depot)
    while q!=200:
            c=100000
            for l in range(0, len(Trucks)):
                if Trucks[l].cost < c :
                    c=Trucks[l].cost
                    index=l
            indexOfTheNextService_locations = -1
            positionOfInsertion = -1
            minimumInsertionCost = 1000000

            for j in range(0, len(service_locations)):
                candidate = service_locations[j]
                if candidate.demand == 0:
                    continue
                for k in range(0, len(Trucks[index].sequenceOfNodes) - 1):
                    before = Trucks[index].sequenceOfNodes[k]
                    after = Trucks[index].sequenceOfNodes[k + 1]
                    if after.id==0:
                        trialCost = matrix[before.id][candidate.id]/35
                    else:
                        costAdded = matrix[before.id][candidate.id]/35+ matrix[candidate.id][after.id]/35
                        costRemoved = matrix[before.id][after.id]/35
                        trialCost = costAdded - costRemoved
                    if candidate.type==1:
                        trialCost += 5/60
                    elif candidate.type==2:
                        trialCost += 15/60
                    else:
                        trialCost += 25/60
                    if ((trialCost < minimumInsertionCost) & (Trucks[index].dem + candidate.demand <= 3000)):
                        indexOfTheNextService_locations = j
                        positionOfInsertion = k
                        minimumInsertionCost = trialCost

            insertedService_locations= service_locations[indexOfTheNextService_locations]
            if insertedService_locations.demand != 0:
                Trucks[index].sequenceOfNodes.insert(positionOfInsertion + 1 , insertedService_locations)
                Trucks[index].cost +=  minimumInsertionCost
                Trucks[index].dem += insertedService_locations.demand
                insertedService_locations.demand = 0
                q+=1
    for l in range(0,len(Trucks)):
        sol.sequenceOfTrucks.append(Trucks[l])
    cost=0
    for i in range (0, len(Trucks)):
        if Trucks[i].cost >cost:
            cost=Trucks[i].cost
    sol.cost=cost


    a = 0

def ReportSolution(sol):
    print(sol.cost , end = '\n ')
    k=0
    for i in range (0, len(sol.sequenceOfTrucks)):
        for j in range (0, len(sol.sequenceOfTrucks[i].sequenceOfNodes)):
            print(sol.sequenceOfTrucks[i].sequenceOfNodes[j].id, end = ',')
            k=k+1
        print( end='\n ')
    print(k,end='\n ')
def CheckSolution(sol, matrix):
    cst = 0
    for i in range(len(sol.sequenceOfTrucks) - 1):
        a = sol.sequenceOfTrucks[i]
        b = sol.sequenceOfTrucks[i+1]
        cst += matrix[a.ID][b.ID]
    if (abs(cst - sol.cost) > 0.00001):
        print('Error')


def solve(m):
    Trucks = m.Trucks
    all_nodes = m.all_nodes
    service_locations = m.service_locations
    depot = all_nodes[0]
    matrix = m.matrix

    sol = Solution()


    #ApplyNearestNeighborMethod(depot, service_locations, sol, matrix,Trucks)
    MinimumInsertions(depot, service_locations, sol, matrix,Trucks)
    #CheckSolution(sol, matrix)
    ReportSolution(sol)
    #SolDrawer.draw(0, sol, all_nodes)

m = Model()
m.BuildModel()
solve(m)



