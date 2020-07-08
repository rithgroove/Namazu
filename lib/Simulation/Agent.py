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
    def __init__(self,name = None):
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
        """
        [Method] setCell
        Set the cell where the agent is standing in.
        
        Parameter:
            - cell : The cell where the agent standing.
        """
        self.currentCell = cell 
        
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