import geopy.distance as distance

class Building:
    def __init__(self,nodes):
        self.nodes = nodes
        lat,lon = 0,0
        for i in nodes:
            lat = i.lat
            lon = i.lon
        lat = lat/nodes.__len__()
        lon = lon/nodes.__len__()        
            
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
    
