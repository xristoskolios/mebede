
from TSP_Model import *

class Solution:
    def __init__(self):
        self.cost = 0.0
        self.sequenceOfTrucks = []

class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9


class Solver:
    def __init__(self, m):
        self.allNodes = m.all_nodes

        self.depot = m.all_nodes[0]


        self.sol = None
        self.bestSolution = None
        self.overallBestSol = None

        self.Trucks = m.Trucks

        self.service_locations = m.service_locations

        self.matrix = m.matrix

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.service_locations)):
            self.service_locations[i].isRouted = False

    def solve(self):

        self.ApplyNearestNeighborMethod()
        cc = self.sol.cost
        print( 'Constr:', self.sol.cost)

        self.LocalSearch()
       # if self.overallBestSol == None or self.overallBestSol.cost > self.sol.cost:
           # self.overallBestSol = self.cloneSolution(self.sol)
        #print( 'Const: ', cc, ' LS:', self.sol.cost, 'BestOverall: ', self.overallBestSol.cost)


        #self.sol = self.overallBestSol
        self.ReportSolution(self.sol)

        return self.sol



    def ApplyNearestNeighborMethod(self):
        self.sol = Solution()
        for l in range(0,len(self.Trucks)):
                self.Trucks[l].sequenceOfNodes.append(self.depot)
        for i in range (0, len(self.service_locations)):
             for l in range(0,len(self.Trucks)):
                    indexOfTheNextService_locations = -1
                    minimumInsertionCost = 100000
                    lastIndexInSolution = len(self.Trucks[l].sequenceOfNodes) - 1
                    lastNodeInTheCurrentSequence = self.Trucks[l].sequenceOfNodes[lastIndexInSolution]

                    for j in range (0, len(self.service_locations)):
                        candidate = self.service_locations[j]
                        if candidate.isRouted == True:
                            continue
                        trialCost = self.matrix[lastNodeInTheCurrentSequence.id][candidate.id]/35
                        if candidate.type==1:
                            trialCost += 5/60
                        elif candidate.type==2:
                            trialCost += 15/60
                        else:
                            trialCost += 25/60
                        if ((trialCost < minimumInsertionCost) & (self.Trucks[l].dem + candidate.demand <= 3000)) :
                            indexOfTheNextService_locations = j
                            minimumInsertionCost = trialCost

                    insertedService_locations = self.service_locations[indexOfTheNextService_locations]
                    if  insertedService_locations.isRouted != True:
                        self.Trucks[l].sequenceOfNodes.append(insertedService_locations)
                        self.Trucks[l].cost += minimumInsertionCost
                        self.Trucks[l].dem += insertedService_locations.demand
                        insertedService_locations.isRouted = True

        for l in range(0,len(self.Trucks)):
            self.Trucks[l].sequenceOfNodes.append(self.depot)
            self.sol.sequenceOfTrucks.append(self.Trucks[l])
        cost=0
        for i in range (0, len(self.Trucks)):
            if self.Trucks[i].cost >cost:
                cost=self.Trucks[i].cost
        self.sol.cost=cost



    def LocalSearch(self):
        self.bestSolution = self.cloneSolution(self.sol)
        terminationCondition = False


        rm = RelocationMove()


        while terminationCondition is False:

            self.InitializeOperators(rm)


            # Relocations

            self.FindBestRelocationMove(rm)
            if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:
                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True


            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution(self.sol)



        self.sol = self.bestSolution


    def cloneTruck(self, rt: Truck):
        cloned = Truck()
        cloned.cost = rt.cost
        cloned.dem = rt.dem
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        return cloned


    def cloneSolution(self, sol: Solution):
        cloned = Solution()
        for i in range(0, len(sol.sequenceOfTrucks)):
            rt = sol.sequenceOfTrucks[i]
            clonedTruck = self.cloneTruck(rt)
            cloned.sequenceOfTrucks.append(clonedTruck)
        cloned.cost = self.sol.cost
        return cloned

    def FindBestRelocationMove(self, rm):
        for i in range(0,len(self.sol.sequenceOfTrucks)):
            for j in range(0,len(self.sol.sequenceOfTrucks[i].sequenceOfNodes)):
                self.matrix[self.sol.sequenceOfTrucks[i].sequenceOfNodes[j].id][self.depot.id]=0
        for originRouteIndex in range(0, len(self.sol.sequenceOfTrucks)):
            rt1: Truck = self.sol.sequenceOfTrucks[originRouteIndex]
            for targetRouteIndex in range(0, len(self.sol.sequenceOfTrucks)):
                rt2: Truck = self.sol.sequenceOfTrucks[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 2):
                    for targetNodeIndex in range(1, len(rt2.sequenceOfNodes) - 2):

                        if originRouteIndex == targetRouteIndex and ( targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            if rt2.dem + B.demand > 3000:
                                continue

                        costAdded = self.matrix[A.id][C.id] + self.matrix[F.id][B.id] + self.matrix[B.id][G.id]
                        costRemoved = self.matrix[A.id][B.id] + self.matrix[B.id][C.id] + self.matrix[F.id][G.id]

                        originRtCostChange = (self.matrix[A.id][C.id] - self.matrix[A.id][B.id] - self.matrix[B.id][C.id])/35
                        targetRtCostChange = (self.matrix[F.id][B.id] + self.matrix[B.id][G.id] - self.matrix[F.id][G.id])/35



                        if B.type == 1:
                                    originRtCostChange -= 5 / 60
                                    targetRtCostChange += 5 / 60

                        elif B.type == 2:
                                    originRtCostChange -= 15 / 60
                                    targetRtCostChange += 15 / 60
                        else:
                                    originRtCostChange -= 25 / 60
                                    targetRtCostChange += 25 / 60


                        moveCost = costAdded/35 - costRemoved/35

                        if (moveCost < rm.moveCost):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, originRtCostChange,
                                                         targetRtCostChange, rm)

    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.sol.sequenceOfTrucks[rm.originRoutePosition]
        targetRt = self.sol.sequenceOfTrucks[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.cost += rm.moveCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.cost += rm.costChangeOriginRt
            targetRt.cost += rm.costChangeTargetRt
            originRt.dem -= B.demand
            targetRt.dem += B.demand



        newCost = self.CalculateTotalCost(self.sol)
        self.sol.cost = newCost


    def CalculateTotalCost(self, sol):
        cost = 0

        for i in range(0, len(sol.sequenceOfTrucks)):

            if self.sol.sequenceOfTrucks[i].cost > cost:
                cost = self.sol.sequenceOfTrucks[i].cost

        return cost

    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost, originRtCostChange, targetRtCostChange, rm:RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex
        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange
        rm.moveCost = moveCost

    def ReportSolution(self ,sol):
        print(sol.cost , end = '\n ')
        k=0
        for i in range (0, len(sol.sequenceOfTrucks)):
            for j in range (0, len(sol.sequenceOfTrucks[i].sequenceOfNodes)):
                print(sol.sequenceOfTrucks[i].sequenceOfNodes[j].id, end = ',')
                k=k+1
            print( end='\n ')
        print(k,end='\n ')

    def InitializeOperators(self, rm):
        rm.Initialize()



