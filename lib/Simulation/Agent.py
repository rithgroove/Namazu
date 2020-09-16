import geopy.distance as gdistance
from .ERI import ERI
from .MovementVector import MovementVector
from .MovementSequence import MovementSequence
import random
class Agent():
    """
    [Class] Agent
    A class to represent an agent in the map. This agent respresent a group of people, not a single person.
    
    Properties:
        - name : The name of the agent, can be anything.
        - resident: A boolean of whether or not this agent is a local resident.
        - familiar : A boolean to mark whether or not this agent is familiar with local area.
        - weak : A boolean to mark whether or not this agent is a slow moving agent (like elderly people).
        - number : number of person in this agent.
        - car : A boolean to mark whether or not this agent travel by car.
        - sound : An integer to mark how far their voice could reach when distributing information.
        - interval : not sure.
        - nextCell : next cell to move to.
        - currentCell : current cell.
        - movingSpeed : Speed in m/s.
        - hasERI : A boolean to mark whether or not this agent have ERI.
        - currentERI : current active ERI.
        - asking : A boolean to mark whether or not this agent asking for ERI.
        - providing : A boolean to mark whether or not this agent is providing ERI.
        - intention : Not used at the moment.
        - evacuationStart : how many steps required until this agent start evacuating.
        - oval : The oval shape to represent this agent in the renderer.
        - transition : (x,y) transition to translate the position of the oval in the next update.
        - evacuated : A boolean to mark whether or not this agent is evacuated.
        - walkedDistanceToNextCell : how many distance the current agent have walked from current cell to the next cell.
        - nextCellDistance : how many distance the current agent needs to walk to reach the next cell.
    """
    def __init__(self,name = None,cellDict={}):
        """
        [Constructor]
        create an agent without a location
        """
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
        self.movingSpeed = 1.46
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
        self.cellDict = cellDict
        self.lat = 0
        self.lon = 0
        self.currentMovementVector = None
        self.activeSequence = None
        self.currentPosition = (0.0,0.0)
        self.WBF= False
        self.evacLeader = False

    def setCell(self,cell):
        """
        [Method] setCell
        Set the cell where the agent is standing in.
        
        Parameter:
            - cell : The cell where the agent standing.
        """
        if (self.currentCell is not None):
            self.currentCell.removeAgent(self)
        self.currentCell = cell 
        self.currentCell.addAgent(self)
        self.currentPosition = cell.getPosition()
        self.lat = cell.lat
        self.lon = cell.lon
        
    def getSpeed(self):
        speed = self.movingSpeed
        if (self.weak):
            speed = min(speed,0.94)
        if (self.currentERI.isEmpty()):
            speed = speed * 0.75
        if self.number > 1:
            speed = speed * (0.95-0.025*self.number)
        return speed

    def getVehicleSpeed():
        speed = 40000.0/3600.0
        return speed
    
    def setERI(self,eri):
        """
        [Method] setERI
        Set the agent ERI (Evacuation Route Information).
        
        Parameter:
            - eri : The ERI the agent holding on.
        """
        self.currentERI = eri
        self.hasERI = True
        
    def calculateTrajectory(self,timestamp = None):
        self.activeSequence = self.currentERI.calculateClosestEvacPoint(self.currentCell,timestamp = timestamp)
    
    def evaluate(self):
        if self.currentCell.isEvacPoint:
            if (self.currentCell.evacPoint.addEvacuees(self)):
                print("Evac Success")
                self.evacuated = True
            else:
                # Add info to knowledge pool
                print("Evacpoint full")
                self.currentERI.disableEvacPoint(self.currentERI.destination)                
        if self.currentCell.blocked:    
            print("Do Nothing Now")
            
    def step(self,steps=1):
        if(self.activeSequence is None or self.activeSequence.finished):
            #check ERI is empty?
            if(self.currentERI.isEmpty()):
                self.nonERIStep()
            else:
                # recalculate closest evac point
                self.activeSequence = self.currentERI.calculateClosestEvacPoint(self.currentCell)
        if self.activeSequence is not None:
            #after recalculate
            leftOver = steps * self.getSpeed()
            
            while leftOver > 0 and not self.activeSequence.finished and not self.evacuated:
                leftOver = self.activeSequence.step(leftOver)
                self.currentCell.removeAgent(self)
                self.currentCell = self.activeSequence.currentCell
                self.currentCell.addAgent(self)
                self.evaluate()
                #print(f"leftover = {leftOver}")
                
            self.transition = self.activeSequence.getVector(self.currentPosition)
            self.lat = self.currentPosition[0] + self.transition[0]
            self.lon = self.currentPosition[1] + self.transition[1]
            self.currentPosition= (self.lat, self.lon)       
            #self.transition = (self.transition[1], self.transition[0])
           
    def nonERIStep(self):
        option = []
        origin = None
        if (self.activeSequence is not None):
            origin = self.activeSequence.lastCell
        for x in self.currentCell.connection:
            if (origin is None or x.osmId != origin.osmId):
                option.append(x)
        if (option.__len__() == 0):
            option.append(origin)
        target = option[random.randint(0, option.__len__()-1)]
        #if (origin is not None):
            #print(f"{origin.osmId} vs {target.osmId}")
        vector = [MovementVector(self.currentCell,target)]
        sequence = MovementSequence(vector,vector[0].distance)
        self.activeSequence = sequence
        
    def haveERI(self):
        return not self.currentERI.isEmpty()
    
    def addERIKnowledge(self,otherERI):
        return self.currentERI.gainKnowledge(otherERI)

    def shareKnowledge(self):
        print(self.haveERI())
        if (self.haveERI()):
            #print(f"wat agentnya punya {self.currentERI.evacPoints.__len__()}")
            #if (self.WBF):
            #    print(f"I'm WBF and and I try to spread knowledge for {self.sound} cell")
            self.spreadKnowledge(self.sound,self.currentCell)
    
    def spreadKnowledge(self,count,currentCell):
        
        if(count > 0):
            for y in currentCell.population:
                #share knowledge here:
                if ( y != self and y.addERIKnowledge(self.currentERI)):
                    print("")
            for x in currentCell.connection:
                self.spreadKnowledge(count-1,x)