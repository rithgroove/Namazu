import geopy.distance as distance

class Road:
    def __init__(self,node1, node2):
        self.name,self.start,self.destination = genName(node1,node2)
        self.length = distance.distance(self.start.getPosition(), self.destination.getPosition()).km * 1000
        
    def getPath(self):
        return (self.start.lat, self.start.lon, self.destination.lat,self.destination.lon)
    
    def getPathForRendering(self):
        return (self.start.lon, self.start.lat, self.destination.lon,self.destination.lat)
        
    def getStartingCoordinate(self):
        return (self.start.lat, self.start.lon)
    
    def getDestinationCoordinate(self):
        return (self.destination.lat,self.destination.lon)
    
    def getVector(self):
        return (self.destination.lat - self.start.lat, self.destination.lon - self.start.lon)
    
    def __str__(self):
        temp = f"({self.start.lat},{self.start.lon}) to ({self.destination.lat},{self.destination.lon}) - {self.length}"
        return temp
    
def genName(node1, node2):
    name = None
    start = None 
    destination = None
    if (node1.osmId < node2.osmId):
        name = f"{node1.osmId}-{node2.osmId}"
        start = node1 
        destination = node2 
    else:
        name = f"{node2.osmId}-{node1.osmId}"        
        start = node2
        destination = node1
    return (name, start, destination)
    