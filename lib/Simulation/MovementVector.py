import geopy.distance as gdistance

class MovementVector:
    
    def __init__(self,startingCell, destinationCell ):
        self.startingCell = startingCell
        self.destinationCell = destinationCell
        self.starting = startingCell.getPosition()
        self.destination = destinationCell.getPosition()
        self.distance = gdistance.distance(self.starting,self.destination).km*1000
        self.passedThroughDistance = 0
        self.totalTranslation = (self.destination[0]-self.starting[0],self.destination[1]-self.starting[1])
        self.currentPosition = self.starting
        self.finished = False
        self.progress = 0.0
        
    def calculateTranslation(self, currentPosition):
        return (self.currentPosition[0] - currentPosition[0], self.currentPosition[1] - currentPosition[1])
        
    def step(self,distances):
        leftOver = distances - (self.distance - self.passedThroughDistance)
        if leftOver < 0:
            leftOver = 0
        self.passedThroughDistance += distances
        if self.passedThroughDistance >= self.distance:
            self.passedThroughDistance = self.distance     
            self.finished = True
        self.progress = float(self.passedThroughDistance)/float(self.distance)
        if (self.progress >= 1):
            self.progress = 1
        lat = self.starting[0] +(self.progress * self.totalTranslation[0])
        lon = self.starting[1] +(self.progress * self.totalTranslation[1])
        self.currentPosition = (lat, lon)
        return leftOver
            