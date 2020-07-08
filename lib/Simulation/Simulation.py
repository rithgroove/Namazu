import geopy.distance as distance
from .Cell import Cell

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
        self.agents = []
        self.evacuatedAgent = []
        self.evacPoints = []
        self.nzMap = nzMap
        self.stepCount = 0
        self.filledEvacPoints = 0
        self.blockedCells = []
        
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
            cell = Cell()
            for x in range(1,noc):
                cell = Cell()
                passed += cellLength
                transition = (roadVector[0]* passed/road.length, roadVector[1] * passed/road.length)
                tempDestination = (starting[0] + transition [0], starting[1] + transition[1])                
                cell.fill(f"{road.name}-{x}",tempDestination[0],tempDestination[1])
                print(cell)
                current = tempDestination
                if (prevCell is not None):
                    prevCell.neighb
                prevCell = cell
            cell = Cell()
            cell.fill(f"{road.name}-{x}",destination[0],destination[1])
            print(cell)
            
        
    
    
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
        