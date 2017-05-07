from node import *
from GUI import *
import numpy as np
import time, math, random

class Field:

    def __init__(self, dim = 1000):
        self.field = [[0 for _ in range(dim)] for _ in range(dim)]
        self.nodes = []
        self.sinks = []

    def addSource(self, pos, token, team = 0):
        node = SourceNode(pos, token, team=team)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos, "red")

    def addSink(self, pos, token, team = 0):
        node = SinkNode(pos, token, team=team)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        self.sinks.append(node)
        gui.add_node(pos)
        gui.add_score()

    def addHPNode(self, pos, team = 1):
        node = HotPotatoNode(pos, team)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos, "orange")

    def addGenericNode(self, pos, nodeFunc):
        node = nodeFunc(pos)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos)

    def addSmartNode(self, pos, team = 1):
        node = SmartNode(pos, team)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos, "cyan")

    def addNoiseNode(self, pos):
        node = NoiseNode(pos)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos, "grey")

    def checkNeighbors(self):
        for node in self.nodes:
            for node2 in self.nodes:
                if (self.isConnected(node, node2)):
                    node.neighbors.append(node2)
                    gui.add_line(node.pos, node2.pos)

    def isConnected(self, n1, n2):
        if n1.team != n2.team:
            return False
        dis = max(math.sqrt(math.pow(n1.pos[0] - n2.pos[0], 2) + math.pow(n1.pos[1] - n2.pos[1], 2)), 1)
        probability = min(2/math.sqrt(dis), 1)

        return dis < 2
        if probability > random.random():
            return True
        else:
            return False

    def step(self):
        self.checkNeighbors()
        for node in self.nodes:
            if node.status == "SEND":
                node.send(None)
        for node in self.nodes:
            msg = node.getMessages()
            gui.update_packets(node.pos, node.readbuffer)
        for node in self.nodes:
            if node.status == "REC":
                node.recieve()
        for node in self.nodes:
            node.update()
            node.neighbors = []
        for i, node in enumerate(self.sinks):
            gui.update_score(i, "Score{} = {}".format(i, node.score))

    def loadConfig(self, filename):
        with open(filename, 'r') as f:
            xdim, ydim = map(int, f.readline().strip().split(" "))
            self.field = [[0 for _ in range(xdim)] for _ in range(ydim)]
            numTypes = int(f.readline().strip())
            types = {}
            types["SINK"] = SinkNode
            types["SOURCE"] = SourceNode
            for _ in range(numTypes):
                typedef = f.readline().strip().split(" ")
                typeIden = typedef[0]
                typeFunc = eval(typedef[1])
                print typeIden, typeFunc
                types[typeIden] = typeFunc

    def __repr__(self):
        out = ""
        for y in self.field:
            l = map(lambda x: x.type if x != 0 else 0, y)
            out += str(l) + "\n"
        return out

test = Field(10)
def loop():
    while True:
        test.step()
        time.sleep(.1)
        print"--------------"
        root.update()

def defaultTest():
    test.addSource((0,0), "test")
    #test.addHPNode((1,1))
    #test.addHPNode((2,2))
    #test.addHPNode((3,4))
    #test.addHPNode((7,1))
    test.addNoiseNode((3, 3))
    test.addSmartNode((1, 1))
    test.addSmartNode((2, 2))
    test.addSmartNode((3, 4))
    test.addSmartNode((7, 1))
    test.addSink((0,1), "test")
    print test
    loop()


def teamTest():
    #test.addSource((0,0), "test", 1)
    #test.addHPNode((0,1), 1)
    #test.addHPNode((0,2), 1)
    #test.addHPNode((0,3), 1)
    #test.addHPNode((0,4), 1)
    #test.addSink((0,5), "test", 1)
    test.addSource((5,5), "test", 2)
    test.addNoiseNode((3, 3))
    test.addSmartNode((1, 1), 2)
    test.addSmartNode((4, 4), 2)
    test.addSmartNode((4, 3), 2)
    test.addSmartNode((3, 4), 2)
    test.addSmartNode((2, 4), 2)
    test.addSmartNode((4, 2), 2)
    test.addSmartNode((2, 2), 2)
    test.addSmartNode((3, 2), 2)
    test.addSmartNode((2, 3), 2)
    test.addSink((3,1), "test", 2)
    print test
    loop()



#test.loadConfig("simpleTest.fld")
root.update()
#defaultTest()
teamTest()
