import geopy.distance as distance
from .MovementVector import MovementVector
from .MovementSequence import MovementSequence
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
        self.token = ""
        
    def initiateEvacPoints(self,evacPoints):
        self.evacPoints = evacPoints
        self.generateToken()

    def generateToken(self):
        self.evacPoints.sort(key=sortEvacPoint)
        self.token = "token"
        for x in self.evacPoints:
            self.token = f"{self.token}-{x.evac_id}"

    def isEmpty(self):
        if (self.evacPoints.__len__() == 0):
            return True
        if (self.evacPoints.__len__() == self.disabledEvacPoints.__len__()): 
            return True
        return False
    
    def calculateClosestEvacPoint(self,currentCell, skipUnimportantEvacPoint=True, timestamp = None):
        self.closestDistance = 127420000#1% of earth diameter
        self.evacPointsDistance = []
        #calculate distance for each evac points        
        for x in self.evacPoints:
            # ignore if evac point is disabled (full etc)
            if (x not in self.disabledEvacPoints):
                result = None 
                # ignore if evac point is disabled (full etc)
                if(skipUnimportantEvacPoint):
                    # Find other evac point that is closer than current closest distance
                    result = searchPath(self.nzMap,self.nzSim,currentCell,x.cell,self.closestDistance)                    
                    self.evacPointsDistance.append(result)
                else:
                    # Force Calculate all
                    result = searchPath(self.nzMap,currentCell,x.cell)                
                    self.evacPointsDistance.append(result)
                if (result[0] != -1 and self.closestDistance > result[0]):
                    self.closestDistance = result[0]
                    self.mainPath = result[1]
                    self.destination = x
        if timestamp is None:
            self.timestamp = self.nzSim.stepCount
        return self.mainPath
                

        #print(self.mainPath)

    def step(self):
        #print(self.mainPath)
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
        if (self.token != otherERI.token):
            for evacPoint in self.evacPoints:
                if (evacPoint not in otherERI.evacPoints):
                    otherERI.addEvacPoint(evacPoint)
                    temp = True
            for disabledEP in self.disabledEvacPoints:
                if (otherERI.disableEvacPoint(disabledEP)):
                    temp = True
        if (temp):
            self.generateToken()
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

def sortEvacPoint(e):
    return e.evac_id

def searchPath(nzMap,nzSim,startingCell,targetCell, limit = None):
    path = []
    quicksearch = {}
    workingList = []
    visited = []
    found = False
    finalNode = None
    distance = -1
    
    #insert starting node as the initial node
    startingNode = AStarNode(startingCell,targetCell)
    workingList.append(startingNode)
    
    #setup known blocked cells
    for x in nzSim.blockedCells:
        x.setBlocked()
        
    #main loop
    while (workingList.__len__() != 0):        
        #get the first in the list
        workingNode = workingList.pop(0)
        workingNode.visited = True
        visited.append(workingNode)
        workingCell = workingNode.cell
        sequence = None
        #start working if the limit is None or there is no path having lower distance than the designated limit
        if (limit is None or workingNode.f < limit):
            #loop through all of the path
            for x in workingCell.connection:
                #find if the a star node is created or not
                temp = quicksearch.get(x.osmId)
                #continue if condition apply
                if ((temp is None or temp not in visited) and not x.tempBlocked):
                    #if not created, create it
                    if temp is None:
                        temp = AStarNode(x,targetCell)
                        quicksearch[temp.name] = temp
                    #calculate value
                    prevValue = temp.f
                    temp.calculateFrom(workingNode)
                    currentValue = temp.f
                    
                    #if destination reached
                    if (x == targetCell):
                        #backtrack to create path
                        finalNode = temp
                        backtracking = finalNode
                        distance = finalNode.f
                        while backtracking != startingNode:
                            #create movement vector
                            movement = MovementVector(backtracking.prevNode.cell, backtracking.cell)
                            backtracking = backtracking.prevNode
                            path.insert(0,movement)
                        found = True
                        sequence = MovementSequence(path,distance)
                        break            
                        
                    #
                    #if (workingList.__len__() == 0):
                    #    workingList.append(temp)
                    #else:
                    
                    # messy method to find the right index to insert it based on value order
                    # remove to re-insert
                    if (temp in workingList):
                        workingList.remove(temp)
                    inserted = False

                    for i in range(0,workingList.__len__()):
                        #insert in the right index
                        if (workingList[i].f > currentValue):
                            workingList.insert(i,temp)
                            inserted = True
                            break
                    #if not inserted yet, it means it's the last index
                    if(not inserted):
                        workingList.append(temp)
        if (found):
            break   
    for x in nzSim.blockedCells:
        x.clear()
    return distance, sequence

   