#!/usr/bin/python

import threading
import time
import random
from .Agent import Agent
from .ERI import ERI
import geopy.distance as distance
exitFlag = 0

class InitializationThread (threading.Thread):
    def __init__(self, threadID, name,agent,simulation,withERI = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.agent = agent
        self.simulation = simulation
        self.agents = []
        self.withERI = withERI
    def run(self):
        print(f"Starting {self.name}")
        self.agents = generateAgent(self.agent,self.simulation,self.name,self.withERI)
        print(f"Exiting {self.name}")
        
def generateAgent(agents,simulation,name,withERI=False):
    tempAgents = []
        #queueLock.acquire()          
    x = 1
    while tempAgents.__len__() < agents:
        randomized = random.randint(0,simulation.cells.__len__()-1)
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
                for i in range(0,1):
                    temp2.append(eps[i][0])
                eri.initiateEvacPoints(temp2)
            temp.setERI(eri)
            temp.calculateTrajectory()
            print(f"{name}->Processing = {x}/{agents} agents")
            x += 1
        else:
            print(f"Selected Cell is out of bounds, selecting another random cell")
    print(f"{name}->finished")
    return tempAgents
        #queueLock.release()
        
