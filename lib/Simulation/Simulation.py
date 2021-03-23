import geopy.distance as distance
from .Cell import Cell
from .EvacuationPoint import EvacuationPoint
from .Agent import Agent
from .ERI import ERI
from .InitializationThread import InitializationThread
import threading
import random
class Simulation():
    """
    [Class] Simulation
    A class to represent a single simulation.
    
    Properties:
        - cells : a single cell used to represent a point in a road. distance between cells will be around 20 meters.
        - agents : list of unevacuated agents.
        - evacuatedAgents : list of evacuated agents
        - evacPoints : list of evacuation Points
        - nzMap : the Map this simulation working in
        - stepCount : number of step at the current moment (goal 1 step = 1 sec)
        - filledEvacPoints : number of evacuation points that is in full capacity
        - blockedCells: List of cells that is currently blocked
    """
    def __init__(self, nzMap):
        self.cells = []
        self.cellDict = {}
        self.agents = []
        self.evacuatedAgent = []
        self.evacPoints = []
        self.nzMap = nzMap
        self.stepCount = 0
        self.filledEvacPoints = 0
        self.blockedCells = []
        self.WBF = []
        
    def buildCells(self,cellLength = 20):        
        for road in self.nzMap.roads:
            #number of cells (road length / 20meter)
            noc = int(road.length / cellLength)
            roadVector = road.getVector()
            
            if noc == 0:
                noc = 1
            passed = 0.0
            starting = road.getStartingCoordinate()
            current = starting
            destination = road.getDestinationCoordinate()
            x = 1
            prevCell = None
            
            cell = self.cellDict.get(f"{road.start.osmId}")
            if (cell is None):
                cell = Cell()
                cell.fill(f"{road.start.osmId}",starting[0],starting[1])
                self.cellDict[f"{road.start.osmId}"] = cell
                self.cells.append(cell)
            cell.addDestination(road.destination)
            cell.addRoad(road)
            prevCell = cell            
            for x in range(1,noc):
                name = f"{road.name}-{x}"
                cell = self.cellDict.get(name)
                if (cell is None):
                    cell = Cell()
                    passed += cellLength
                    transition = (roadVector[0]* passed/road.length, roadVector[1] * passed/road.length)
                    tempDestination = (starting[0] + transition [0], starting[1] + transition[1])                
                    cell.fill(name,tempDestination[0],tempDestination[1])
                    self.cellDict[name] = cell
                    self.cells.append(cell)
                    current = tempDestination
                if (prevCell is not None):
                    prevCell.addNeighbor(cell)
                    cell.addNeighbor(prevCell)
                cell.addDestination(road.start)
                cell.addDestination(road.destination)
                cell.addRoad(road)
                prevCell = cell
                
            cell = self.cellDict.get(f"{road.destination.osmId}")
            if (cell is None):
                cell = Cell()
                cell.fill(f"{road.destination.osmId}",destination[0],destination[1])
                self.cellDict[f"{road.destination.osmId}"] = cell
                self.cells.append(cell)
            if (prevCell is not None):
                prevCell.addNeighbor(cell)
                cell.addNeighbor(prevCell)
            cell.addDestination(road.start)
            cell.addRoad(road)
        self.restructureRoad()
        self.nzMap.recalculateGrid()
        
    def restructureRoad(self):
        allRoads = []
        i = 0 
        while self.cells.__len__() > 0:
            i +=1
            queue = []
            roadGroup = []
            workingOn = self.cells.pop(0)
            roadGroup.append(workingOn)
            queue.append(workingOn)
            while (queue.__len__() > 0):
                workingOn = queue.pop(0)
                for x in workingOn.connection:
                    if (x in self.cells):
                        self.cells.remove(x)
                        if (x not in roadGroup):
                            roadGroup.append(x)
                        if (x not in queue):
                            queue.append(x)
            allRoads.append(roadGroup)
        max = 0 
        for x in allRoads:
            if (x.__len__() > max):
                self.cells = x
                max = x.__len__()
                
        for cell in self.cells:
            if(self.nzMap.distanceLat is not None and self.nzMap.distanceLon is not None):
                xAxis = int((cell.lon-self.nzMap.minlon)/self.nzMap.distanceLon)
                yAxis = int((cell.lat-self.nzMap.minlat)/self.nzMap.distanceLat)
                if xAxis >= self.nzMap.gridSize[0]:
                    xAxis = self.nzMap.gridSize[0]-1
                if yAxis >= self.nzMap.gridSize[1]:
                    yAxis = self.nzMap.gridSize[1]-1
                self.nzMap.grids[xAxis][yAxis].addCell(cell)
                
    def step(self,steps = 15):
        #print("Stepping each agent")
        self.stepCount +=1
        for x in self.agents:
            temp = x.evacuated
            x.step(steps)
            if (temp != x.evacuated):
                self.evacuatedAgent.append(x)      
        for x in self.WBF:
            x.shareKnowledge()
        for x in self.agents:
            x.shareKnowledge()
        self.filledEvacPoints = 0 
        for x in self.evacPoints:
            if (x.occupancy == x.capacity):
                self.filledEvacPoints += 1      
        
        #self.shareInfo()
                
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
    
    def initialize(self,agents, agentsWithERI, evac, capacity, numberOfThread = 3, WBF_count  = 40):
        self.evacPoints = []
        evac_id = 1
        while self.evacPoints.__len__() < evac:
            #set 12 capacity for now
            cell = self.cells[random.randint(0,self.cells.__len__())]
            if not cell.outOfBounds:
                temp = EvacuationPoint(evac_id,cell,capacity)
                self.evacPoints.append(temp)
                cell.isEvacPoint = True
                cell.evacPoint = temp 
        self.agents = []
        
        #generate agent without ERI
        threadList = []
        for x in range(1,numberOfThread+1):
            threadList.append(f"Thread-{x}")
        threads = []
        threadID = 1

        for tName in threadList:
            thread = InitializationThread(threadID, tName, int(agents/numberOfThread),self,False,False)
            thread.start()
            threads.append(thread)
            threadID += 1

        for t in threads:
            t.join()
            print(t.agents.__len__())
            self.agents.extend(t.agents)
        print("Finished generating agents Without ERI")
        
        #generate agent with ERI
        threadList = []
        for x in range(1,numberOfThread+1):
            threadList.append(f"Thread-{x}")
        threads = []
        threadID = 1

        for tName in threadList:
            thread = InitializationThread(threadID, tName, int(agentsWithERI/numberOfThread),self,True,False)
            thread.start()
            threads.append(thread)
            threadID += 1

        for t in threads:
            t.join()
            print(t.agents.__len__())
            self.agents.extend(t.agents)
        print("Finished generating agents With ERI")
        
        #generate evacuation leader agent
        threadList = []
        for x in range(1,numberOfThread+1):
            threadList.append(f"Thread-{x}")
        threads = []
        threadID = 1

        for tName in threadList:
            thread = InitializationThread(threadID, tName, int(agentsWithERI/numberOfThread),self,True,True)
            thread.start()
            threads.append(thread)
            threadID += 1

        for t in threads:
            t.join()
            print(t.agents.__len__())
            self.agents.extend(t.agents)
        print("Finished generating evac-leader")
        
        
        #generate WBF
        threadList = []
        for x in range(1,numberOfThread+1):
            threadList.append(f"Thread-{x}")
        threads = []
        threadID = 1
        
        for tName in threadList:
            thread = InitializationThread(threadID, tName, int(WBF_count/numberOfThread),self,True)
            thread.start()
            threads.append(thread)
            threadID += 1

        for t in threads:
            t.join()
            print(t.agents.__len__())
            self.WBF.extend(t.agents)
        print("Finished generating WBF")
        
        for x in self.WBF:
            x.WBF = True
            x.movingSpeed = 0.0
            x.sound = 10
            print(x)
        
        self.blockedCells = []
        x = 1
    
    
def generateAgent(agents,simulation,name,withERI=False):
    tempAgents = []
    while tempAgents.__len__() < agents:
        randomized = random.randint(0,simulation.cells.__len__())
        cell = simulation.cells[randomized]
        #print(cell)            
        if not cell.outOfBounds:
            temp = Agent(f"agent-{name}-{x}",simulation.cellDict)
            #set one person
            temp.number = 1
            temp.setCell(cell)
            cell.population.append(temp)
            tempAgents.append(temp)
            eri = ERI(simulation.nzMap,simulation)
            if withERI:
                eps = []
                for ep in simulation.evacPoints:
                    epDistance = distance.distance(ep.cell.getPosition(),cell.getPosition()).km
                    eps.append((ep, epDistance))
                eps.sort(key=lambda tup: tup[1])
                temp2 = []
                for i in range(0,0):
                    temp2.append(eps[i][0])
                eri.initiateEvacPoints(temp2)
            temp.setERI(eri)
            temp.calculateTrajectory()
            print(f"Processing = {x}/{agents} agents")
            x += 1
        else:
            print(f"Selected Cell is out of bounds, selecting another random cell")
        