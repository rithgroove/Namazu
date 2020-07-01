class Cell():
    """
    [Class] Cell
    A class to represent a cell in the map
    
    Properties:
        - connection : List of all connected cells
        - connectionWeight : list of all weights for the connection
        - destination : List of nodes this cell pointing to
        - population : List of all agent in this cell (Might be removed later)
        - outOfBounds : Mark this cell as out of the rendering area
        - osmId : the Open Street Map ID of this cell. If there's no Open streetmap ID, 
                  it will be generated automatically with format 
                  (Lower_destination_id+_+higher_destination_id+_+incremental_id)
        - lat : latitude of this cell
        - lon : longitude of this cell
        - tags : Not used at the moment, but planned as a list of tags for cell
        - blocked : A boolean used to represent whether or not this cell is blocked.
        - tempBlocked : A boolean used to temporary block this cell when calculating A-Star function
    """
    
    def __init__(self):
        """Initialize an empty cell"""
        self.connection = []
        self.connectionWeight = []
        self.destination = []
        self.population = []
        self.outOfBounds = False
        self.osmId = None
        self.lat = None
        self.lon = None
        self.tags = None
        self.blocked = False
        self.tempBlocked = False
        
    def fill (self,osmId,lat,lon):
        """Fill the latitude, longitude and the Open Street Map ID
        
        Parameter:
        osmId = the Open Street Map ID
        lat = the cell's latitude
        lon = the cell's longitude
        
        """
        self.lat = lat
        self.lon = lon
        self.osmId = f"{osmId}"
        
    def __str__(self):
        """Print the cell"""
        tempstring = f"id: {self.osmId}\nlat = {self.lat} lon = {self.lon} \nNeighbor : \n"
        for neighbor in self.connection:
            tempstring = tempstring + f"\t{neighbor.osmId} : {neighbor.lat}, {neighbor.lon}\n"
        return tempstring
    
    def setTempBlockedStatus(self):
        """set the current temporary blocked status to the real_blocked"""
        self.tempBlocked = self.blocked
        
    def releaseTempBlockedStatus(self):
        """reset the current temporary blocked status"""
        self.tempBlocked = False
    
    def initializeWeight(self):
        """initialize weight for every network"""
        self.connectionWeight = np.zeros(())

    def getPosition(self):
        """get the latitude and longitude of the cell"""
        return (self.lat,self.lon);