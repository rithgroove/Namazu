import tkinter 
import platform


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
OS = platform.system()
animating = False



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
    canvas.scan_dragto(viewPort[0], viewPort[1], gain=1)
    #draw()
    #print("Mouse position: (%s %s)" % (event.x, event.y))
    #print("Root position: (%s %s)" % (event.x_root, event.y_root))
    return

def clickRelease(event):
    global prevPosition
    prevPosition = None

def doubleClick(event):
    global animating
    animating = not animating
    
def step():
    global animating
    if (animating):
        sim.step()
        print("finish stepping")
        for x in sim.agents:
            moveAgent(x)
        
    canvas.after(1000,step)
        
def scroll(event):
    global canvas
    global viewPort
    global scale
    value = -1*(event.delta)
    #print(f"Scrolling {value}")
    if OS == 'Linux':
        if event.num == 4:
            canvas.scale('all', 0, 0, 1.1, 1.1)
            scale *=  1.1
        elif event.num == 5:
            canvas.scale('all', 0, 0, 10.0/11.0, 10.0/11.0)
            scale *= (10.0/11.0)
    else:          
        if (value > 0):
            canvas.scale('all', 0, 0,1.1, 1.1)
            scale *=  1.1
        elif (value <0):
            canvas.scale('all', 0, 0, 10.0/11.0, 10.0/11.0)
            scale *= (10.0/11.0)

#def resize(event):
    #global canvas
    #region = canvas.bbox(tkinter.ALL)
    #print(region)
    #windowsSize = (,)
    #canvas.configure(scrollregion=region)      
            
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
            
    for temp in osmMap.roads:
        data = temp.getPathForRendering()
        
        x =  (data[0] - canvasOrigin[0]) * scale +viewPort[0]
        y = (canvasSize[1]-(data[1] - canvasOrigin[1])) * scale + viewPort[1]
        #drawCircle(temp.lon,temp.lat,1, "#476042")
        x1 = (data[2] - canvasOrigin[0]) * scale +viewPort[0]
        y1 = (canvasSize[1]-(data[3] - canvasOrigin[1])) * scale + viewPort[1]
        canvas.create_line(x,y,x1,y1)
        
    for temp in osmMap.roadNodes:
        drawCircle(temp.lon,temp.lat,1, "#476042")        
            
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
        drawCircle(temp.lon, temp.lat, 3,"#0000FF")
        

def drawAgent():   
    for cell in sim.cells:
        drawCircle(cell.lon,cell.lat,2, "#999999")
    #for temp in sim.blockedCells:
    #    drawCircle(temp.cell.lon,temp.cell.lat,5, "#CC3333")
    for evacPoint in sim.evacPoints:
        drawCircle(evacPoint.cell.lon, evacPoint.cell.lat, 10,"#33CCCC")
    for agent in sim.agents:
        if (agent.evacLeader):
            agent.oval = drawCircle(agent.currentCell.lon, agent.currentCell.lat, 5,"#CCCC33", agent.name)  
        elif (agent.haveERI()):
            agent.oval = drawCircle(agent.currentCell.lon, agent.currentCell.lat, 5,"#00FF00", agent.name)         
        else:
            agent.oval = drawCircle(agent.currentCell.lon, agent.currentCell.lat, 5,"#CC33CC", agent.name)      
    for agent in sim.WBF:
        agent.oval = drawCircle(agent.currentCell.lon, agent.currentCell.lat, 5,"#0000FF", agent.name)         

def moveAgent(agent):
    x = agent.transition[1] * scale
    y = agent.transition[0]  * scale * -1
    #print((x,y,agent.oval))
    if (agent.evacLeader):
        canvas.itemconfig(agent.oval,fill="#CCCC33")
    elif (agent.haveERI()):
        canvas.itemconfig(agent.oval,fill="#00FF00")
    else:
        canvas.itemconfig(agent.oval,fill="#CC33CC")        
    canvas.move(agent.oval,x,y)

def drawCircle(lon,lat,radius, color, name = None):
    x = (lon - canvasOrigin[0]) * scale +viewPort[0]
    y = (canvasSize[1]-( lat - canvasOrigin[1])) * scale + viewPort[1]
    circle = None
    if (name is None):
        circle = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill= color)
    else:
        circle = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color,tag = name)
    return circle

def drawLine(originLon,originLat, destinationLon, destinationLat, color, name = None):
    x = (lon - canvasOrigin[0]) * scale +viewPort[0]
    y = (canvasSize[1]-( lat - canvasOrigin[1])) * scale + viewPort[1]
    circle = None
    if (name is None):
        circle = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill= color)
    else:
        circle = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color,tag = name)
    return circle

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
    root.resizable(False,False)
    canvas = tkinter.Canvas(root)
    ## bind button
    canvas.bind("<B1-Motion>", motion)
    canvas.bind("<ButtonRelease-1>",clickRelease)
    canvas.bind("<Double-Button-1>",doubleClick)
    canvas.bind("<MouseWheel>", scroll)
    #canvas.bind("<Configure>", resize)
    if OS == "Linux":
        root.bind_all('<4>', scroll, add='+')
        root.bind_all('<5>', scroll, add='+')
    else:
        # Windows and MacOS
        root.bind_all("<MouseWheel>", scroll, add='+')
    canvas.pack()
    canvas.config(width=windowSize[0], height=windowSize[1])
        
    draw()
    if (path is not None):
        drawPath(path)
    if (sim is not None):
        drawAgent()
        
    canvas.after(1000,step)
    root.mainloop()