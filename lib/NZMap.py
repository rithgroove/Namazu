import xml.etree.ElementTree as ET
import os
import osmium
import geopy.distance as distance

class Map(osmium.SimpleHandler):
    def __init__(self):
        osmium.SimpleHandler.__init__(self)
        self.num_nodes = 0
        self.num_ways = 0
        self.num_cells = 0
        self.nodesDict = {}
        self.waysDict = {}
        self.cellsDict = {}
        self.buildings = []
        self.naturals = []
        self.nodes = []
        self.leisures = []
        self.amenities = []
        self.ways = []
        self.cells = []
        self.minlat = 0
        self.minlon = 0
        self.maxlat = 0
        self.maxlon = 0 

    def changeSet(self, n):
        print(n)
        
    def node(self, n):
        self.num_nodes += 1
        temp =  Node()
        temp.fill(n)
        self.nodesDict[f"n{n.id}"] = temp
        self.nodes.append(temp)
        
    def way(self, n):
        self.num_ways += 1
        temp =  Way()
        temp.fill(n,self.nodesDict)
        self.waysDict[f"n{n.id}"] = temp
        self.ways.append(temp)
        
    def setBounds(self,filepath):
        tree = ET.parse(filepath)
        root = tree.getroot()
        for child in root:
            if (child.tag == 'bounds'):
                self.minlat = child.attrib['minlat']
                self.maxlat = child.attrib['maxlat']
                self.minlon = child.attrib['minlon']
                self.maxlon = child.attrib['maxlon']
                break
                
    def generateCells(self):
        for x in self.ways:
            notRoad = False
            if 'building' in x.tags.keys():
                notRoad = True
                self.buildings.append(x)
            if 'natural' in x.tags.keys():
                notRoad = True
                self.naturals.append(x)
            if 'leisure' in x.tags.keys():
                notRoad = True
                self.leisures.append(x)
            if 'amenity' in x.tags.keys():
                notRoad = True
                self.amenities.append(x)
            if (not notRoad):
                prevNode = None
                prevCell = None              
                for node in x.nodes:
                    cell = self.cellsDict.get(f"{node.osmId}")
                    if cell is None:
                        cell = Cell()
                        cell.fill(node.osmId,node.lat,node.lon)
                        self.cellsDict[cell.osmId] = cell
                        self.cells.append(cell)
                        self.num_cells += 1
                    if prevNode is not None:
                        #calculate how much cells between 2 node
                        coords1 = (prevNode.lat,prevNode.lon)
                        coords2 = (node.lat,node.lon)
                        coords_distance = distance.distance(coords1, coords2).km * 1000
                        cellnumber = int(coords_distance/ 20)
                        not_generated = True

                        #check if the path between 2 nodes have been generated before
                        for temp in prevCell.destination:
                            if (temp.osmId == cell.osmId):
                                not_generated = False
                                break

                        #if not generate
                        if not_generated:
                            if (prevCell is not None):
                                prevCell.destination.append(cell)
                                cell.destination.append(prevCell)
                            localPrev = prevCell
                            for i in range(1,cellnumber):
                                #use the id as the name (lowest id in front)
                                inbetween_cell_name = f"{min(prevCell.osmId,cell.osmId)}-{max(prevCell.osmId,cell.osmId)}-{i}"
                                #just incase check if the inbetween id is exist, probably not, but just to make sure.
                                inbetween_cell = self.cellsDict.get(inbetween_cell_name)
                                if (inbetween_cell is None):
                                    inbetween_cell = Cell()
                                    lat = prevCell.lat + (float(i)/cellnumber *(cell.lat-prevCell.lat))
                                    lon = prevCell.lon + (float(i)/cellnumber *(cell.lon-prevCell.lon))
                                    inbetween_cell.fill(inbetween_cell_name,lat,lon)
                                    self.cellsDict[inbetween_cell_name] = inbetween_cell
                                    self.cells.append(inbetween_cell)
                                    self.num_cells += 1
                                    localPrev.connection.append(inbetween_cell)
                                    inbetween_cell.connection.append(localPrev)
                                    inbetween_cell.destination.append(cell)
                                    inbetween_cell.destination.append(prevCell)
                                localPrev = inbetween_cell
                            localPrev.connection.append(cell)
                            cell.connection.append(localPrev)
                    prevCell = cell
                    prevNode = node
                
class Node():    
    def __init__(self):
        self.lat = 0.0
        self.lon = 0.0
        self.tags = {}
        self.connections = []
        self.isroad = False
        self.ways = {}
        self.osmId = ""
        
    def fill(self, osmNode):
        self.osmId = osmNode.id
        self.lat = osmNode.location.lat
        self.lon = osmNode.location.lon
        for tag in osmNode.tags:
            self.tags[tag.k] = tag.v
        
    def addWay(self,way):
        self.ways[way.osmId] = way
        
    def addConnection(self,connection):
        self.connections.append(connection)
            
    def __str__(self):
        tempstring = f"id: {self.osmId}\nlat = {self.lat} lon = {self.lon} \nnumber of ways : {self.ways.__len__()}\nnumber of connections : {self.connections.__len__()}\nTags : \n"
        for key in self.tags.keys():
            tempstring = tempstring + f"\t{key} : {self.tags[key]}\n"
        tempstring = tempstring + "\n"
        return tempstring
    
class Way():
    def __init__(self):
        self.tags = {}
        self.nodes = []    
        self.osmId = ""
        
    def fill(self, osmWay, nodes):
        self.osmId = osmWay.id

        for node in osmWay.nodes:
            temp = nodes[f"n{node.ref}"]
            if (temp is not None):
                self.nodes.append(temp)
                temp.addWay(self)
            else:
                print("\n\nNode not Found\n\n")
            
        for tag in osmWay.tags:
            self.tags[tag.k] = tag.v
            
    def __str__(self):
        tempstring = f"id: {self.osmId}\nnumber of nodes : {self.nodes.__len__()}\nTags : \n"
        for key in self.tags.keys():
            tempstring = tempstring + f"\t{key} : {self.tags[key]}\n"
        tempstring = tempstring + "\n"
        return tempstring
    
class Cell():
    def __init__(self):
        self.connection = []
        self.destination = []
        self.osmId = None
        self.lat = None
        self.lon = None
    def fill (self,osmId,lat,lon):
        self.lat = lat
        self.lon = lon
        self.osmId = osmId;
        
def readFile(filepath):
    generatedMap = Map()
    generatedMap.apply_file(filepath)
    generatedMap.setBounds(filepath)
    generatedMap.generateCells()
    return generatedMap