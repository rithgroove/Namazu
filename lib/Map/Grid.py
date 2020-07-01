class Grid():  
    """
    [Class] Node
    A class to represent the Open Street Map Node.
    
    Properties:
        - minlat : minimum latitude.
        - minlon : minimum longitude.
        - maxlat : maximum latitute.
        - maxlon : maximum longitude.
        - nodes : 
    """
    
    def __init__(self):
        """
        [Constructor]
        Initialize an empty node.
        """
        self.minlat = 0.0
        self.minlon = 0.0
        self.maxlat = 0.0
        self.maxlon = 0.0
        self.nodes = 0.0