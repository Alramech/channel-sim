from node import *
from GUI import *
import numpy as np
import time

class Field:

    def __init__(self, dim = 1000):
        self.field = [[0 for _ in range(dim)] for _ in range(dim)]
        self.nodes = []
        self.sinks = []

    def addSource(self, pos, token):
        node = SourceNode(pos, token)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos, "red")

    def addSink(self, pos, token):
        node = SinkNode(pos, token)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        self.sinks.append(node)
        gui.add_node(pos)
        gui.add_score()

    def addHPNode(self, pos):
        node = HotPotatoNode(pos)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos, "orange")

    def addGenericNode(self, pos, nodeFunc):
        node = nodeFunc(pos)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        gui.add_node(pos)

    def checkNeighbors(self):
        for node in self.nodes:
            for node2 in self.nodes:
                if (self.isConnected(node, node2)):
                    node.neighbors.append(node2)
                    gui.add_line(node.pos, node2.pos)

    def isConnected(self, n1, n2):
        return True

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
        time.sleep(1)
        print"--------------"
        root.update()

def defaultTest():
    test.addSource((0,0), "test")
    test.addHPNode((1,1))
    test.addHPNode((2,2))
    test.addHPNode((3,4))
    test.addHPNode((7,1))
    test.addSink((0,1), "test")
    test.addSink((9,9), "test")
    print test
    loop()

#test.loadConfig("simpleTest.fld")
root.update()
defaultTest()
