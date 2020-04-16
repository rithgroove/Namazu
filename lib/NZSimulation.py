import geopy.distance as distance

class Agent():
    def __init__(self):
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
        
class evacPoint():
    def __init__(self, capacity):
        self.cell = cell
        self.capacity = capacity
        self.currentEvacuees = 0
        
class ERI():
    def __init__(self,nzmap):
        self.evacuationInfo = {}
        self.blockedCell = {}
        self.blockedConnection = {}
        self.nzmap = nzmap
    
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
    
def searchPath(nzMap,startingCell,targetCell):
    path = []
    quicksearch = {}
    workingList = []
    startingNode = AStarNode(startingCell,targetCell)
    workingList.append(startingNode)
    visited = []
    found = False
    finalNode = None
    latestValue = 0
    traverseValue = {}
    traverseValue[startingCell.osmId] = 0;
    while (workingList.__len__() != 0):
        workingNode = workingList.pop(0)
        workingNode.visited = True
        visited.append(workingNode)
        traverseValue[workingNode.cell.osmId] = 1;
        workingCell = workingNode.cell
        print(workingCell)
        search = "5400722235"
        for x in workingCell.connection:
            
            if (x.osmId not in traverseValue.keys()):
                traverseValue[x.osmId] = 0;
            if (search is not None and x.osmId == search):
                print("found the searched")

            temp = quicksearch.get(x.osmId)
            if (temp is None or temp not in visited):

                if temp is None:
                    temp = AStarNode(x,targetCell)
                    quicksearch[temp.name] = temp
                if (search is not None and x.osmId == search):
                    print("is not none and have not visited")

                prevValue = temp.f
                temp.calculateFrom(workingNode)
                currentValue = temp.f
                if (x == targetCell):
                    finalNode = temp
                    backtracking = finalNode
                    path.insert(0,backtracking.cell)
                    while backtracking != startingNode:
                        backtracking = backtracking.prevNode
                        path.insert(0,backtracking.cell)
                    #don't forget to handle something here
                    found = True
                    break            
                #print(f"{prevValue} vs {currentValue}")
                #if (prevValue != currentValue):
                if (workingList.__len__() == 0):
                    #print(f"inserting node {workingList.__len__()}")
                    if (search is not None and x.osmId == search):
                        print("Working list empty so insert")
                    workingList.append(temp)
                else:
                    if (temp in workingList):
                        #print(f"removing node {workingList.__len__()}")
                        if (search is not None and x.osmId == search):
                            print("remove from working list")
                        workingList.remove(temp)
                    inserted = False
                    for i in range(0,workingList.__len__()):
                        if (workingList[i].f > currentValue):
                            #print(f"inserting node {workingList.__len__()}")
                            if (search is not None and x.osmId == search):
                                print("insert in the middle")
                            inserted = True
                            workingList.insert(i,temp)
                            break
                    if(not inserted):
                        workingList.append(temp);                        
                        if (search is not None and x.osmId == search):
                            print("insert to the end")

        if (found):
            break            
    if (not found):
        print("gak ketemu coy")
    return (path,traverseValue)
    
   