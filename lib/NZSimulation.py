import geopy.distance as distance
import random
class Simulation():
    def __init__(self, nzMap):
        self.agents = []
        self.evacPoints = []
        self.nzMap = nzMap
        self.stepCount = 0
        
    def initialize(self,agents, evac):
        for x in range(0,evac):
            #set 5 capacity for now
            temp = evacPoint(self.nzMap.roads[random.randint(0,self.nzMap.roads.__len__())],5)
            self.evacPoints.append(temp)
        for x in range(0,agents):
            temp = Agent(f"agent-{x}")
            #set one person
            temp.number = 1
            randomized = random.randint(0,self.nzMap.roads.__len__())
            #print(randomized)
            cell = self.nzMap.roads[randomized]
            #print(cell)
            temp.setCell(cell)
            cell.population.append(temp)
            self.agents.append(temp)
            eri = ERI(self.nzMap)
            eri.updateEvacPoints(self.evacPoints)
            temp.setERI(eri)
            temp.calculateTrajectory()
            print(f"Processing = {x+1}/{agents} agents")
            
    def step(self):
        #print("Stepping each agent")
        for x in self.agents:
            x.step()
            self.stepCount +=1
            
    def __str__(self):
        temp = f"Total agent = {self.agents.__len__()}\n"
        temp = f"{temp}Total Evac Point = {self.evacPoints.__len__()}\n"
        return temp
        
        
class Agent():
    def __init__(self,name = None):
        self.name = name 
        self.resident = True
        self.familiar = True
        self.weak = False
        self.number = 1
        self.car = False
        self.sound = 2
        self.interval = 0
        self.currentCell = None
        self.movingSpeed = 1
        self.hasERI = False
        self.currentERI = None
        self.asking = True
        self.providing = False
        self.intention = None
        self.evacuationStart = None
        self.oval = None
        self.transition = (0,0)
        
    def setCell(self,cell):
        self.currentCell = cell 
        
    def setERI(self,eri):
        self.currentERI = eri
        self.hasERI = True
        
    def calculateTrajectory(self):
        self.currentERI.calculateClosestEvacPoint(self.currentCell)
    
    def step(self):
        #print(f"\n\nCurrent Cell : \n{self.currentCell}")
        self.transition = (0,0)
        nextCell = self.currentERI.step()
        if (nextCell is not None):
            #print(f"\nMoving To : \n{nextCell}")
            cell = self.currentCell
            self.transition = (nextCell.lon-cell.lon, nextCell.lat - cell.lat)
            self.currentCell = nextCell
            nextCell.population.append(self)
            cell.population.remove(self)
            #print(self.transition)
        
class evacPoint():
    def __init__(self,cell, capacity):
        self.cell = cell
        self.capacity = capacity
        self.currentEvacuees = 0
        
class ERI():
    def __init__(self,nzMap):
        self.evacPoints = []
        self.blockedCell = {}
        self.blockedConnection = {}
        self.nzMap = nzMap
        self.timestamp = None
        self.mainPath = None
        self.destination = None
        self.closestDistance = 127420000
    def updateEvacPoints(self,evacPoints):
        self.evacPoints = evacPoints
        #don't forget to update timestamp later
    def calculateClosestEvacPoint(self,currentCell, skipUnimportantEvacPoint=True):
        self.closestDistance = 127420000#1% of earth diameter
        for x in self.evacPoints:
            result = None 
            if(skipUnimportantEvacPoint):
                result = searchPath(self.nzMap,currentCell,x.cell,self.closestDistance)
            else:
                result = searchPath(self.nzMap,currentCell,x.cell)                
            if (result[0] != -1 and self.closestDistance > result[0]):
                self.closestDistance = result[0]
                self.mainPath = result[1]
    def step(self):
        if (self.mainPath is None or self.mainPath.__len__() == 0):
            return None
        return self.mainPath.pop(0)
    
    def __str__(self):
        test = f"Distance = {self.closestDistance}\nDestination: \n{self.mainPath[-1]}"
        return test
        
    
class AStarNode():
    def __init__(self,cell,targetCell):
        self.g = 0
        self.h = 0
        self.position = (cell.lat,cell.lon)
        self.name = cell.osmId
        self.cell = cell
        self.visited = False
        self.prevNode = None
        dft =  distance.distance(self.position, (targetCell.lat,targetCell.lon)).km * 1000
        self.h = dft
        self.f = self.g + self.h
        self.g = -1
        
    def calculateFrom(self,prevNode):
        if (not self.visited):
            distanceToPrevious = 0
            distanceFromOrigin = 0
            distanceToPrevious = prevNode.g
            distanceFromOrigin = distance.distance(self.position, prevNode.position).km * 1000
            distanceFromOrigin += distanceToPrevious
            if (self.g > distanceFromOrigin or self.g == -1):
                self.g = distanceFromOrigin
                self.prevNode = prevNode
                self.f = self.g + self.h
    
def searchPath(nzMap,startingCell,targetCell, limit = None):
    path = []
    quicksearch = {}
    workingList = []
    startingNode = AStarNode(startingCell,targetCell)
    workingList.append(startingNode)
    visited = []
    found = False
    finalNode = None
    distance = -1
    while (workingList.__len__() != 0):
        workingNode = workingList.pop(0)
        workingNode.visited = True
        visited.append(workingNode)
        workingCell = workingNode.cell
        #print(workingCell)
        if (limit is None or workingNode.f < limit):
            for x in workingCell.connection:

                temp = quicksearch.get(x.osmId)
                if (temp is None or temp not in visited):

                    if temp is None:
                        temp = AStarNode(x,targetCell)
                        quicksearch[temp.name] = temp
                    prevValue = temp.f
                    temp.calculateFrom(workingNode)
                    currentValue = temp.f
                    if (x == targetCell):
                        finalNode = temp
                        backtracking = finalNode
                        distance = finalNode.f
                        path.insert(0,backtracking.cell)
                        while backtracking != startingNode:
                            backtracking = backtracking.prevNode
                            path.insert(0,backtracking.cell)
                        found = True
                        break            
                    if (workingList.__len__() == 0):
                        workingList.append(temp)
                    else:
                        if (temp in workingList):
                            workingList.remove(temp)
                        inserted = False
                        for i in range(0,workingList.__len__()):
                            if (workingList[i].f > currentValue):
                                inserted = True
                                workingList.insert(i,temp)
                                break
                        if(not inserted):
                            workingList.append(temp);                        
        if (found):
            break   
    
    return distance,path
    
   