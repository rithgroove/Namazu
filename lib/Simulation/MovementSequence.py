class MovementSequence:
    
    def __init__(self,sequence,totalDistance):
        self.sequence = sequence
        self.currentActiveVector = None
        self.totalDistance = totalDistance
        self.currentTraversedDistance = 0
        self.finished = False
        self.currentCell = sequence[0].startingCell
        self.lastCell = sequence[0].startingCell
        #print(self.sequence.__len__())
        
    def step(self,distances):
        # pop from array of current active se
        if (self.currentActiveVector is None or self.currentActiveVector.finished) and self.sequence.__len__()>0:
            #print(self.sequence.__len__())
            self.currentActiveVector = self.sequence.pop(0)     
        leftOver = 0
        translation = (0.0,0.0)
        if (self.currentActiveVector.finished):
            leftOver = distances
            self.finished = True
        else:
            leftOver = self.currentActiveVector.step(distances)            
            self.currentTraversedDistance += (distances-leftOver)                        
            if self.currentActiveVector.finished:
                self.lastCell = self.currentCell
                self.currentCell = self.currentActiveVector.destinationCell
        return leftOver
        
    def getVector(self,currentPosition):
        return self.currentActiveVector.calculateTranslation(currentPosition)
        