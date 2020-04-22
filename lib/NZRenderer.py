import tkinter 


osmMap = None
sim = None
windowSize = (1024,768)
viewPort = (0,0)
canvasOrigin = None
canvasMax = None
canvasSize = None
scale = None 
prevPosition = None
canvas = None


def motion(event):
    global prevPosition
    global viewPort
    global canvas
    global canvasSize
    global windowSize
    if prevPosition is not None:
        translation = (prevPosition[0]-event.x, prevPosition[1]-event.y)
        viewPort = (viewPort[0]-translation[0], viewPort[1]- translation[1])
        #print(translation)
        if (viewPort[0] > 0):
            viewPort = (0, viewPort[1])
        elif (viewPort[0] < -1* scale *canvasSize[0] + windowSize[0]):
            #print("too far x")
            viewPort = (int( -1* scale *canvasSize[0] + windowSize[0]),viewPort[1])
        if (viewPort[1] > 0):
            viewPort = (viewPort[0], 0)
        elif (viewPort[1] < -1* scale *canvasSize[1] + windowSize[1]):
            #print("too far y")
            viewPort = (viewPort[0], int( -1* scale *canvasSize[1] + windowSize[1]))
        
    prevPosition = (event.x,event.y)
    #print(viewPort[0], viewPort[1])
    canvas.scan_dragto(viewPort[0], viewPort[1], gain=1)
    #draw()
    #print("Mouse position: (%s %s)" % (event.x, event.y))
    #print("Root position: (%s %s)" % (event.x_root, event.y_root))
    return

def clickRelease(event):
    global prevPosition
    prevPosition = None

def doubleClick(event):
    sim.step()
    print("finish stepping")
    for x in sim.agents:
        moveAgent(x)


    
def draw():
            
    for temp in osmMap.amenities:
        path = []
        for node in temp.nodes:
            x = (node.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            outline = '#CCCCCC'
            fill = '#DDDDDD'
            
            if (temp.tags['amenity'] == 'school'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'police'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'karaoke_box'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'university'):
                outline = '#619e44'
                fill = '#9edd80'
            elif (temp.tags['amenity'] == 'library'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'driving_school'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'bus_station'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'kindergarten'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'post_office'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'community_centre'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'toilets'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'bank'):
                outline = '#515464'
                fill = '#CCCCCC'
            elif (temp.tags['amenity'] == 'parking'):
                outline = '#515464'
                fill = '#676768'
            elif (temp.tags['amenity'] == 'bicycle_parking'):
                outline = '#515464'
                fill = '#676768'
            elif (temp.tags['amenity'] == 'parking_space'):
                outline = '#515464'
                fill = '#676768'
                
            canvas.create_polygon(path, outline=outline,
            fill=fill, width=1)
    for temp in osmMap.leisures:
        path = []
        for node in temp.nodes:
            x = (node.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            outline = '#CCCCCC'
            fill = '#DDDDDD'
            if (temp.tags['leisure'] == 'park'):
                outline = '#619e44'
                fill = '#9edd80'
            elif (temp.tags['leisure'] == 'garden'):
                outline = '#85a22f'
                fill = '#b7da52'
            elif (temp.tags['leisure'] == 'track'):
                outline = '#7a651d'
                fill = '#c4a646'
            elif (temp.tags['leisure'] == 'pitch'):
                outline = '#7a651d'
                fill = '#c4a646'
                
            canvas.create_polygon(path, outline=outline,
            fill=fill, width=1)
            
    for temp in osmMap.naturals:
        path = []
        for node in temp.nodes:
            x = (node.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            outline = '#CCCCCC'
            fill = '#DDDDDD'
            if (temp.tags['natural'] == 'grassland'):
                outline = '#619e44'
                fill = '#9edd80'
            elif (temp.tags['natural'] == 'water'):
                outline = '#515464'
                fill = '#8895e4'
            elif (temp.tags['natural'] == 'wood'):
                outline = '#2c7509'
                fill = '#42b00d'
            elif (temp.tags['natural'] == 'scrub'):
                outline = '#85a22f'
                fill = '#b7da52'
            elif (temp.tags['natural'] == 'heath'):
                outline = '#7a651d'
                fill = '#c4a646'
                
            canvas.create_polygon(path, outline=outline,
            fill=fill, width=1)

    for temp in osmMap.buildings:
        path = []
        for node in temp.nodes:
            x = (node.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( node.lat - canvasOrigin[1])) * scale + viewPort[1]
            path.append(x)
            path.append(y)
        if (path.__len__() > 6):
            canvas.create_polygon(path, outline='#515464',
            fill='#CCCCCC', width=2)
            
    for temp in osmMap.cells:
        x =  (temp.lon - canvasOrigin[0]) * scale +viewPort[0]
        y = (canvasSize[1]-( temp.lat - canvasOrigin[1])) * scale + viewPort[1]
        canvas.create_oval(x-1, y-1, x+1, y+1, fill="#476042")
        for connection in temp.connection:
            x1 = (connection.lon - canvasOrigin[0]) * scale +viewPort[0]
            y1 = (canvasSize[1]-( connection.lat - canvasOrigin[1])) * scale + viewPort[1]
            canvas.create_line(x, y, x1, y1)
            
            
    for temp2  in osmMap.ways:
        for temp in temp2.nodes:
            if temp.tags.keys().__len__() == 0:
                #print(temp.tags)
                x =  (temp.lon - canvasOrigin[0]) * scale +viewPort[0]
                y = (canvasSize[1]-( temp.lat - canvasOrigin[1])) * scale + viewPort[1]
                canvas.create_oval(x-2, y-2, x+2, y+2, fill="#33CC33")
            
def drawPath(path):
    prev = None
    for temp in path:
        if (prev is not None):            
            x =  (temp.lon - canvasOrigin[0]) * scale +viewPort[0]
            y = (canvasSize[1]-( temp.lat - canvasOrigin[1])) * scale + viewPort[1]
            x1 = (prev.lon - canvasOrigin[0]) * scale +viewPort[0]
            y1 = (canvasSize[1]-( prev.lat - canvasOrigin[1])) * scale + viewPort[1]
            canvas.create_line(x, y, x1, y1,fill="#0000FF")
        prev = temp
    for temp in path:
        x =  (temp.lon - canvasOrigin[0]) * scale +viewPort[0]
        y = (canvasSize[1]-( temp.lat - canvasOrigin[1])) * scale + viewPort[1]
        canvas.create_oval(x-3, y-3, x+3, y+3, fill="#0000FF")
        
def drawAgent():
    for evacPoint in sim.evacPoints:
        x =  (evacPoint.cell.lon - canvasOrigin[0]) * scale +viewPort[0]
        y = (canvasSize[1]-(evacPoint.cell.lat - canvasOrigin[1])) * scale + viewPort[1]
        canvas.create_oval(x-10, y-10, x+10, y+10, fill="#3333CC")
    for agent in sim.agents:
        #print(agent.currentCell)
        x =  (agent.currentCell.lon - canvasOrigin[0]) * scale +viewPort[0]
        y = (canvasSize[1]-( agent.currentCell.lat - canvasOrigin[1])) * scale + viewPort[1]
        agent.oval = canvas.create_oval(x-5, y-5, x+5, y+5, fill="#CC3333",tag = agent.name)

def moveAgent(agent):
    x = agent.transition[0] * scale
    y = agent.transition[1]  * scale * -1
    #print((x,y,agent.oval))
    canvas.move(agent.oval,x,y)
    
def render(map,simulation = None, path = None):
    global osmMap
    global canvasOrigin
    global canvasMax
    global canvasSize
    global canvas
    global scale
    global windowSize
    global viewPort
    global sim
    sim = simulation
    osmMap = map
    canvasOrigin = (float(osmMap.minlon),float(osmMap.minlat))
    canvasMax = (float(osmMap.maxlon),float(osmMap.maxlat))
    canvasSize = (float(osmMap.maxlon)-float(osmMap.minlon),float(osmMap.maxlat)-float(osmMap.minlat))
    scale = 100000 
    windowSize = (1024,768)
    viewPort = (0,0)
    prevPosition = None
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root)
    canvas.bind("<B1-Motion>", motion)
    canvas.bind("<ButtonRelease-1>",clickRelease)
    canvas.bind("<Double-Button-1>",doubleClick)
    canvas.pack()
    canvas.config(width=windowSize[0], height=windowSize[1])
    draw()
    if (path is not None):
        drawPath(path)
    if (sim is not None):
        drawAgent()
    root.mainloop()