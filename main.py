#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     17/11/2014
# Copyright:   (c) Timothy 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import pygame, sys, os, random
    import pygame.freetype
    clock = pygame.time.Clock()
    pygame.init()
    FPS = 6
    DEVPINK = (255,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (0,255,255)
    BLACK = (0,0,0)
    GREY = (128,128,128)
    WHITE = (255,255,255)
    nodeCount = 20
    windowHeight = 1000
    windowWidth = 1500
    nodeRadius = 5
    nodeThickness = 0
    edgeThickness = 1
    mainSurface = pygame.display.set_mode((windowWidth,windowHeight))
    pygame.freetype.init()
    fontsize = 16
    boxFontSize = 24
    writeFont = pygame.freetype.SysFont('Consolas',fontsize,True,0)
    boxWriteFont = pygame.freetype.SysFont('Consolas',boxFontSize,0,0)
    gridSurface = pygame.image.load('grid.png')
    lastOrder = 0
    lowestTemporary = 0
    lowestTempNode = Node
    minimumDistance = 100
    connectionProbability = 0.2

    nodeArray = []
    edgeArray = []
    finalEdgeArray = []

    #state variables
    simStage = 1

    while True:
        mainSurface.fill(BLACK)

        if simStage == 1:
            nodeArray.append(Node(100,100,BLUE))
            nodeArray.append(Node(windowWidth - 100, windowHeight - 100,GREEN))
            for i in range(2,nodeCount):
                goodNode = False
                nodeArray.append(Node(random.randint(1,windowWidth - 100),random.randint(100,windowHeight),WHITE))
                while goodNode == False:
                    goodNode = True
                    for node in nodeArray:
                        if node == nodeArray[i]:
                            pass
                        else:
                            if distanceBetween(node,nodeArray[i]) < minimumDistance:
                                goodNode = False
                    if goodNode == False:
                        nodeArray[i].xPos = random.randint(1,windowWidth - 100)
                        nodeArray[i].yPos = random.randint(100,windowHeight)

            simStage = 2
        elif simStage == 2: #generating edges
            for i in range(0,nodeCount):
                for j in range(i + 1, nodeCount):
                    if i == 0 and j == 1:
                        pass
                    else:
                        if random.random() < connectionProbability:
                            newEdge = Edge(nodeArray[i],nodeArray[j])
                            edgeArray.append(newEdge)
                            nodeArray[i].edgeArray.append(newEdge)
                            nodeArray[j].edgeArray.append(newEdge)
            simStage = 3
        elif simStage == 3:
            clock.tick(0.5)
            nodeArray[0].permanent = 0
            nodeArray[0].order = lastOrder + 1
            lastOrder = lastOrder + 1
            for each in nodeArray[0].edgeArray:
                if each.node2 == nodeArray[0]:
                    each.node1.temporary = nodeArray[0].permanent + each.value
                elif each.node1 == nodeArray[0]:
                    each.node2.temporary = nodeArray[0].permanent + each.value
            simStage = 4
        elif simStage == 4:
            lowestTemporary = 99999
            for node in nodeArray:
                if node.temporary < lowestTemporary and node.order == 90210:
                    lowestTemporary = node.temporary
                    lowestTempNode = node
            nodeArray[nodeArray.index(lowestTempNode)].order = lastOrder + 1
            nodeArray[nodeArray.index(lowestTempNode)].permanent = lowestTempNode.temporary
            lastOrder = lastOrder + 1
            simStage = 5
            pygame.draw.circle(mainSurface,GREY,(lowestTempNode.xPos,lowestTempNode.yPos),15,0)
        elif simStage == 5:
            pygame.draw.circle(mainSurface,GREY,(lowestTempNode.xPos,lowestTempNode.yPos),15,0)
            for edge in lowestTempNode.edgeArray:
                if edge.node1 == lowestTempNode:
                    if edge.node2.order == 90210:
                        if lowestTempNode.permanent + edge.value < edge.node2.temporary:
                            edge.node2.temporary = lowestTempNode.permanent + edge.value
                elif edge.node2 == lowestTempNode:
                    if edge.node1.order == 90210:
                        if lowestTempNode.permanent + edge.value < edge.node1.temporary:
                            edge.node1.temporary = lowestTempNode.permanent + edge.value
            if lastOrder == nodeCount:
                simStage = 6
            else:
                simStage = 4
        elif simStage == 6:
            finalNode = nodeArray[1]
            simStage = 7
        elif simStage == 7:
            for edge in finalNode.edgeArray:
                if edge.node1 == finalNode:
                    if edge.node2.permanent == finalNode.permanent - edge.value:
                        finalEdgeArray.append(edge)
                        if edge.node2 == nodeArray[0]:
                            simStage = 8
                        else:
                            finalNode = edge.node2
                elif edge.node2 == finalNode:
                    if edge.node1.permanent == finalNode.permanent - edge.value:
                        finalEdgeArray.append(edge)
                        if edge.node1 == nodeArray[0]:
                            simStage = 8
                        else:
                            finalNode = edge.node1
        else:
            pass



        boxWriteFont.render_to(mainSurface,(5,5),'simStage = ' + str(simStage),WHITE)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        for edge in edgeArray:
            pygame.draw.line(mainSurface,WHITE,(edge.xPos1,edge.yPos1),(edge.xPos2,edge.yPos2),edgeThickness)
            writeFont.render_to(mainSurface,(int((edge.xPos1 + edge.xPos2) / 2),(int((edge.yPos1 + edge.yPos2)) / 2) - int(fontsize / 2)),str(edge.value),WHITE)
        for edge in finalEdgeArray:
            pygame.draw.line(mainSurface,GREEN,(edge.xPos1,edge.yPos1),(edge.xPos2,edge.yPos2),5)
            writeFont.render_to(mainSurface,(int((edge.xPos1 + edge.xPos2) / 2),(int((edge.yPos1 + edge.yPos2)) / 2) - int(fontsize / 2)),str(edge.value),WHITE)
        for node in nodeArray:
            pygame.draw.circle(mainSurface,node.colour,(node.xPos,node.yPos),nodeRadius,nodeThickness)
            mainSurface.blit(gridSurface,(node.xPos,node.yPos - 70))
            if node.order == 90210:
                pass
            else:
                boxWriteFont.render_to(mainSurface,(node.xPos + 37,node.yPos - 65),str(node.order),WHITE)
            if node.temporary == 90210:
                pass
            else:
                boxWriteFont.render_to(mainSurface,(node.xPos + 5, node.yPos - 33),str(node.temporary),WHITE)
            if node.permanent == 90210:
                pass
            else:
                boxWriteFont.render_to(mainSurface,(node.xPos + 5, node.yPos - 65),str(node.permanent),WHITE)

        pygame.display.update()
        clock.tick(FPS)
def distanceBetween(entity1,entity2):
    return (((entity1.xPos - entity2.xPos)**2) + ((entity1.yPos - entity2.yPos)**2))**0.5
class Node():
    xPos = 0
    yPos = 0
    order = 90210
    temporary = 90210
    permanent = 90210
    colour = (0,0,0)
    edgeArray = []
    def __init__(self,xPos,yPos,colour):
        self.xPos = xPos
        self.yPos = yPos
        self.colour = colour
class Edge():
    xPos1 = 0
    xPos2 = 0
    yPos1 = 0
    yPos2 = 0
    node1 = Node
    node2 = Node
    value = 0
    def __init__(self,node1,node2):
        import random
        self.xPos1 = node1.xPos
        self.yPos1 = node1.yPos
        self.xPos2 = node2.xPos
        self.yPos2 = node2.yPos
        self.node1 = node1
        self.node2 = node2
        self.value = random.randint(1,25)
if __name__ == '__main__':
    from pygame.locals import *
    main()
