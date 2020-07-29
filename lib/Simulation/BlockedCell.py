class BlockedCell():
    def __init__(self,cell):
        self.cell = cell
    def setBlocked(self):
        self.cell.tempBlocked = True
    def clear(self):    
        self.cell.tempBlocked = False
        