import xml.etree.ElementTree as ET
import os
import osmium
import numpy
import geopy.distance as distance
from .Node import  Node
from .Way import Way
from .Road import Road
from .Road import genName

class Map(osmium.SimpleHandler):
    """
    [Class] Map
    A class to represent the map
    
    Properties:
        - minlat : minimum latitude.
        - minlon : minimum longitude.
        - maxlat : maximum latitute.
        - maxlon : maximum longitude.
        - num_nodes : Number of Nodes.
        - nodesDict : Dictionary of all nodes. The key used are the Open Street Map ID.
        - nodes : List of all nodes.
        - num_ways : Number of Ways.
        - waysDict : Dictionary of all nodes. The key used are the Open Street Map ID.
        - ways : List of all ways.
        - roadsDict : List of all nodes that marked as road.
        - roads : List of all roads.
    """
    def __init__(self):
        """
        [Constructor]    
        Generate Empty Map.
        """
        osmium.SimpleHandler.__init__(self)
        self.minlat = 0
        self.minlon = 0
        self.maxlat = 0
        self.maxlon = 0
        
        self.num_nodes = 0
        self.num_nodes = 0
        self.nodesDict = {}
        self.nodes = []
        
        self.num_ways = 0
        self.waysDict = {}
        self.ways = []
        
        self.num_roads = 0
        self.roadNodesDict = {}
        self.roadNodes = []             
        self.roadsDict = {}
        self.roads = []             
        self.num_buildings = 0
        self.buildings = []
        
        self.naturals = []
        self.leisures = []
        self.amenities = []
        self.others = []
        
    def node(self, n):
        """
        [Method] node
        Do not use this method, this is an override method from osmium to generate node.
        """
        self.num_nodes += 1
        temp =  Node()
        temp.fill(n)
        self.nodesDict[f"n{n.id}"] = temp
        self.nodes.append(temp)
        
    def way(self, n):
        """
        [Method] way
        Do not use this method, this is an override method from osmium to generate way.
        """
        self.num_ways += 1
        temp =  Way()
        temp.fill(n,self.nodesDict)
        self.waysDict[f"n{n.id}"] = temp
        self.ways.append(temp)
        
    def __str__(self):
        """
        [Method] __str__
        Generate the Map Statistic string and return it.
        
        Return: [string] String of summarized map Information.
        """
        tempstring = f"Namazu Map\n number of nodes = {self.num_nodes}\n number of ways = {self.num_ways}\n"
        tempstring = tempstring + f" number of roads = {self.roads.__len__()}\n"
        tempstring = tempstring + f" number of roads node = {self.roadNodes.__len__()}\n number of building = {self.buildings.__len__()}"
        return tempstring
    
    def setBounds(self,filepath):
        """
        [Method] __str__
        Setup the bounds using the file path
        
        Parameter:
            - filepath : path to the OSM file
        """
        tree = ET.parse(filepath)
        root = tree.getroot()
        for child in root:
            if (child.tag == 'bounds'):
                self.minlat = float(child.attrib['minlat'])
                self.maxlat = float(child.attrib['maxlat'])
                self.minlon = float(child.attrib['minlon'])
                self.maxlon = float(child.attrib['maxlon'])
                break
                
    def constructMap(self):
        """
        [Method] constructMap
        Method to construct the Map. This method will separate which nodes are roads and which 
        
        """
        for x in self.ways:
            if 'building' in x.tags.keys():
                self.buildings.append(x)
            elif 'natural' in x.tags.keys():
                self.naturals.append(x)
            elif 'leisure' in x.tags.keys():
                self.leisures.append(x)
            elif 'amenity' in x.tags.keys():
                self.amenities.append(x)
            elif 'highway' in x.tags.keys():
                self.processRoad(x)
            else :
                self.others.append(x)
                
    def processRoad(self,road):
        """
        [Method] processRoad
        Method to link the node based on the open street map ways
        
        Parameter:
            - road: Open Street Map Road.
        """
        startingNode = None
        for node in road.nodes:
            if (startingNode is not None):
                startingNode.addConnection(node)
                node.addConnection(startingNode)           
                roadObject = self.roadsDict.get(genName(startingNode,node)[0])
                if roadObject is None:
                    roadObject = Road(startingNode,node)
                    self.roadsDict[roadObject.name] = roadObject
                    self.roads.append(roadObject)                                    
                
            node.addWay(road)
            startingNode = node
            temp = self.roadNodesDict.get(f"{node.osmId}")
            if temp is None:
                self.roadNodesDict[node.osmId] = node
                self.roadNodes.append(node)
               
            
def readFile(filepath):
    """
    [Function] readFile
    Function to generate map fom osm File
    
    parameter:
        - filepath : path to the OSM file
    """
    generatedMap = Map()
    generatedMap.apply_file(filepath)
    generatedMap.setBounds(filepath)
    generatedMap.constructMap()
    return generatedMap