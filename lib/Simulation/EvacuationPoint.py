import geopy.distance as distance
import random
class EvacuationPoint():
    def __init__(self,evac_id,cell, capacity):
        self.evac_id = evac_id
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
    
    def quickDistance(self, origin):
        return distance.distance(self.cell.getPosition(),origin)