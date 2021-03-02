import geopy.distance as distance

class Building:
    def __init__(self,way):
        self.way = way
        self.lat,self.lon = 0,0
        for i in range(0,way.nodes.__len__()-1):
            self.lat += way.nodes[i].lat
            self.lon += way.nodes[i].lon
        self.lat = self.lat/(way.nodes.__len__()-1)
        self.lon = self.lon/(way.nodes.__len__()-1)
            
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
    
