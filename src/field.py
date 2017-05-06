from node import *
import numpy as np
import time

class Field:

    def __init__(self, dim = 1000):
        self.field = [[0 for _ in range(dim)] for _ in range(dim)]
        self.nodes = []

    def addSource(self, pos, token):
        node = SourceNode(pos, token)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)

    def addSink(self, pos, token):
        node = SinkNode(pos, token)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)

    def addHPNode(self, pos):
        node = HotPotatoNode(pos)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)

    def checkNeighbors(self):
        for node in self.nodes:
            for node2 in self.nodes:
                if (self.isConnected(node, node2)):
                    node.neighbors.append(node2)

    def isConnected(self, n1, n2):
        return True

    def step(self):
        self.checkNeighbors()
        for node in self.nodes:
            if node.status == "SEND":
                node.send(None)
        for node in self.nodes:
            if node.status == "REC":
                node.recieve()
        for node in self.nodes:
            node.update()
            node.neighbors = []

    def __repr__(self):
        out = ""
        for y in self.field:
            l = map(lambda x: x.type if x != 0 else 0, y)
            out += str(l) + "\n"
        return out
test = Field(10)
test.addSource((0,0), "test")
test.addHPNode((1,1))
test.addHPNode((2,2))
test.addHPNode((3,4))
test.addHPNode((7,1))
test.addSink((0,1), "test")
print test
while True:
    test.step()
    time.sleep(1)
    print"--------------"
