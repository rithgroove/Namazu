import geopy.distance as distance
import random
class Simulation():
    def __init__(self, nzMap):
        self.agents = []
        self.evacuatedAgent = []
        self.evacPoints = []
        self.nzMap = nzMap
        self.stepCount = 0
        self.filledEvacPoints = 0
        self.blockedCells = []
        
    def initialize(self,agents, evac, numberOfBlockedCell = 10):
        self.evacPoints = []
        while self.evacPoints.__len__() < evac:
            #set 12 capacity for now
            cell = self.nzMap.roads[random.randint(0,self.nzMap.roads.__len__())]
            if not cell.outOfBounds:
                temp = evacPoint(cell,500)
                self.evacPoints.append(temp)
        self.agents = []
        x = 1
        while self.agents.__len__() < agents:
            temp = Agent(f"agent-{x}")
            #set one person
            temp.number = 1
            randomized = random.randint(0,self.nzMap.roads.__len__())
            #print(randomized)
            cell = self.nzMap.roads[randomized]
            #print(cell)            
            if not cell.outOfBounds:
                temp.setCell(cell)
                cell.population.append(temp)
                self.agents.append(temp)
                eri = ERI(self.nzMap,self)
                eps = []
                for ep in self.evacPoints:
                    epDistance = distance.distance(ep.cell.getPosition(),cell.getPosition()).km
                    eps.append((ep, epDistance))
                eps.sort(key=lambda tup: tup[1])
                temp2 = []
                for i in range(0,3):
                    temp2.append(eps[i][0])
                eri.initiateEvacPoints(temp2)
                temp.setERI(eri)
                temp.calculateTrajectory()
                print(f"Processing = {x}/{agents} agents")
                x += 1
            else:
                print(f"Selected Cell is out of bounds, selecting another random cell")
        self.blockedCells = []
        
        while self.blockedCells.__len__() < numberOfBlockedCell:
            temp = Agent(f"agent-{x}")
            #set one person
            temp.number = 1
            randomized = random.randint(0,self.nzMap.roads.__len__())
            #print(randomized)
            cell = self.nzMap.roads[randomized]
            cell.blocked = True
            #print(cell)            
            if not cell.outOfBounds:
                self.blockedCells.append(BlockedCell(cell))
            
            
    def step(self):
        #print("Stepping each agent")
        self.stepCount +=1
        for x in self.agents:
            temp = x.evacuated
            x.step()
            if (temp != x.evacuated):
                self.evacuatedAgent.append(x)        
        self.filledEvacPoints = 0 
        for x in self.evacPoints:
            if (x.occupancy == x.capacity):
                self.filledEvacPoints += 1                
        self.shareInfo()
                
    def shareInfo(self):
        affectedAgent =[]
        for x in self.agents:
            if (not x.evacuated and x.currentCell.population.__len__() > 1):
                for y in x.currentCell.population:
                    if (x != y and not y.evacuated):
                        result = x.shareKnowledge(y)
                        if(result and y not in affectedAgent):
                            affectedAgent.append(y);
        if (affectedAgent.__len__() > 0):
            temp = f"{affectedAgent.__len__()} number of agents got new knowledge"
        for x in affectedAgent:
            x.calculateTrajectory()
    
    def __str__(self):
        temp = f"Step count = {self.stepCount}\n"
        temp = f"{temp}Total agent = {self.agents.__len__()}\n"
        temp = f"{temp}\tTotal Unevacuated = {self.agents.__len__()-self.evacuatedAgent.__len__()}\n"
        temp = f"{temp}\tTotal Evacuated = {self.evacuatedAgent.__len__()}\n"        
        temp = f"{temp}Total Evac Point = {self.evacPoints.__len__()}\n"
        temp = f"{temp}\tTotal Filled Evac Point = {self.filledEvacPoints}\n"
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
        self.nextCell = None
        self.currentCell = None
        self.movingSpeed = 1.4
        self.hasERI = False
        self.currentERI = None
        self.asking = True
        self.providing = False
        self.intention = None
        self.evacuationStart = None
        self.oval = None
        self.transition = (0,0)
        self.evacuated = False
        self.walkedDistanceToNextCell = 0
        self.nextCellDistance = 0
        
    def setCell(self,cell):
        self.currentCell = cell 
        
    def setERI(self,eri):
        self.currentERI = eri
        self.hasERI = True
        
    def calculateTrajectory(self,timestamp = None):
        self.currentERI.calculateClosestEvacPoint(self.currentCell,timestamp = timestamp)
    
    def step(self):
        #print(f"\n\nCurrent Cell : \n{self.currentCell}")
        self.transition = (0,0)
        if (self.nextCell is None):    
            nextCell = self.currentERI.step()
            self.nextCell = nextCell
            self.nextCellDistance = self.currentERI.calculateNextDistance(self.currentCell)
            self.walkedDistanceToNextCell = 0
            
        if (self.nextCellDistance == self.walkedDistanceToNextCell):            
            nextCell = self.nextCell
            if (nextCell is not None):
                #print(f"\nMoving To : \n{nextCell}")
                if (nextCell.blocked):
                    print("found a blocked cell")
                    temp = BlockedCell(nextCell)
                    self.currentERI.addBlockedCell(temp)
                    self.calculateTrajectory()
                    self.nextCellDistance = 0
                    self.walkedDistanceToNextCell = 0
                else:
                    cell = self.currentCell
                    #self.transition = (nextCell.lon-cell.lon, nextCell.lat - cell.lat)
                    self.currentCell = nextCell
                    nextCell.population.append(self)
                    cell.population.remove(self)
                    self.nextCell = None
                #print(self.transition)
            else:
                #if (self.currentCell == self.currentERI):
                if (not self.evacuated):
                    if (self.currentERI.destination.addEvacuees(self)):
                        print("Evac Success")
                        self.evacuated = True
                        self.nextCellDistance = 0
                        self.walkedDistanceToNextCell = 0
                    else:
                        print("Evacpoint full, finding next evac point")
                        self.currentERI.disableEvacPoint(self.currentERI.destination)
                        self.currentERI.getNewEvacPointInformation(self)
                        self.calculateTrajectory()
                        self.nextCellDistance = 0
                        self.walkedDistanceToNextCell = 0
        else:
            cell = self.currentCell
            tempTransition = self.movingSpeed
            if (self.nextCellDistance- self.walkedDistanceToNextCell < self.movingSpeed):
                self.walkedDistanceToNextCell = self.nextCellDistance
                tempTransition = self.nextCellDistance - self.walkedDistanceToNextCell
            else:
                self.walkedDistanceToNextCell += self.movingSpeed
            percentage = float(tempTransition) / float(self.nextCellDistance)
            self.transition = ((self.nextCell.lon-cell.lon)*percentage, (self.nextCell.lat - cell.lat)*percentage)
            #print(self.transition)
            
                    
    def shareKnowledge(self, agent):
        return self.currentERI.shareKnowledge(agent.currentERI)
        
    
class evacPoint():
    def __init__(self,cell, capacity):
        self.cell = cell
        self.capacity = capacity
        self.occupancy = 0
        self.agents = []
    def addEvacuees(self,agent):
        if agent.number <= (self.capacity - self.occupancy):
            self.agents.append(agent)
            self.occupancy += agent.number
            return True
        return False
    
class BlockedCell():
    def __init__(self,cell):
        self.cell = cell
    def setBlocked(self):
        self.cell.tempBlocked = True
    def clear(self):    
        self.cell.tempBlocked = False
        
class ERI():
    def __init__(self,nzMap,nzSim):
        self.evacPoints = []
        self.evacPointsDistance = []
        self.blockedCell = []
        self.nzMap = nzMap
        self.nzSim = nzSim
        self.timestamp = None
        self.mainPath = None
        self.destination = None
        self.closestDistance = 127420000
        self.disabledEvacPoints = []
    def initiateEvacPoints(self,evacPoints):
        self.evacPoints = evacPoints
        #don't forget to update timestamp later
        
    def calculateClosestEvacPoint(self,currentCell, skipUnimportantEvacPoint=True, timestamp = None):
        self.closestDistance = 127420000#1% of earth diameter
        self.evacPointsDistance = []
        for x in self.evacPoints:
            if (x not in self.disabledEvacPoints):
                result = None 
                if(skipUnimportantEvacPoint):
                    result = searchPath(self.nzMap,self.nzSim,currentCell,x.cell,self.closestDistance)
                    self.evacPointsDistance.append(result)
                else:
                    result = searchPath(self.nzMap,currentCell,x.cell)                
                    self.evacPointsDistance.append(result)
                if (result[0] != -1 and self.closestDistance > result[0]):
                    self.closestDistance = result[0]
                    self.mainPath = result[1]
                    self.destination = x
        if timestamp is None:
            self.timestamp = self.nzSim.stepCount
                
    def step(self):
        if (self.mainPath is None or self.mainPath.__len__() == 0):
            return None
        return self.mainPath.pop(0)
    
    def calculateNextDistance(self,origin):
        if (self.mainPath is None or self.mainPath.__len__() == 0):
            return 0
        return distance.distance(origin.getPosition(),self.mainPath[0].getPosition()).km*1000
    
    def __str__(self):
        test = f"Distance = {self.closestDistance}\nDestination: \n{self.mainPath[-1]}"
        return test
    
    def disableEvacPoint(self,evacPoint):
        if (evacPoint not in self.disabledEvacPoints):
            self.disabledEvacPoints.append(evacPoint)
            return True
        return False
        
    def getNewEvacPointInformation(self,agent):
        eps = []
        for ep in self.nzSim.evacPoints: 
            if (ep not in self.evacPoints):
                epDistance = distance.distance(ep.cell.getPosition(),agent.currentCell.getPosition()).km
                eps.append((ep, epDistance))
        if (eps.__len__() > 0):
            eps.sort(key=lambda tup: tup[1])
            self.evacPoints.append(eps[0][0])
        
    def addEvacPoint(self,evacPoint):
        self.evacPoints.append(evacPoint)
        
    def addBlockedCell(self,blockedCellInstance):
        self.blockedCell.append(blockedCellInstance)
        
    def shareKnowledge(self, otherERI):
        temp = False
        for evacPoint in self.evacPoints:
            if (evacPoint not in otherERI.evacPoints):
                otherERI.addEvacPoint(evacPoint)
                temp = True
        for disabledEP in self.disabledEvacPoints:
            if (otherERI.disableEvacPoint(disabledEP)):
                temp = True
        return temp

    
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
    
def searchPath(nzMap,nzSim,startingCell,targetCell, limit = None):
    path = []
    quicksearch = {}
    workingList = []
    startingNode = AStarNode(startingCell,targetCell)
    workingList.append(startingNode)
    visited = []
    found = False
    finalNode = None
    distance = -1
    for x in nzSim.blockedCells:
        x.setBlocked()
    while (workingList.__len__() != 0):
        workingNode = workingList.pop(0)
        workingNode.visited = True
        visited.append(workingNode)
        workingCell = workingNode.cell
        #print(workingCell)
        if (limit is None or workingNode.f < limit):
            for x in workingCell.connection:
                temp = quicksearch.get(x.osmId)
                if ((temp is None or temp not in visited) and not x.tempBlocked):

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
    for x in nzSim.blockedCells:
        x.clear()
    
    
    return distance,path
    
   