import geopy.distance as distance
import random

def evaluate(sim,limit= None):
    finished = True
    for x in sim.agents:
        if not x.evacuated:
            finished = False
            break
    if limit is not None and sim.stepCount >= limit:
        finished = True
    return finished