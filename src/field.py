from __future__ import division
from GUI import *
from node import *
import numpy as np
import time, math, random

class Stats():

    def __init__(self):
        self.team = 0
        self.numhops = []
        self.interference = []
        self.sent = 0
        self.ratio = []

stats = {}

class Field:

    def __init__(self, dim = 1000):
        self.field = [[0 for _ in range(dim)] for _ in range(dim)]
        self.nodes = []
        self.sinks = []
        self.sources = []
        self.stats = Stats()

    def addSource(self, pos, token, team = 0):
        node = SourceNode(pos, token, team=team)
        self.field[pos[0]][pos[1]] = node
        self.nodes.append(node)
        self.sources.append(node)
        gui.add_node(pos, "red")
        gui.add_sent()

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
        dis = max(math.sqrt(math.pow(n1.pos[0] - n2.pos[0], 2) + math.pow(n1.pos[1] - n2.pos[1], 2)), 1)
        probability = min(2/math.sqrt(dis), 1)

        if n2.type == "Noise":
            return False
        return dis < 2
        print probability
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
        print test.nodes
        for node in self.nodes:
            if node.status == "REC":
                node.recieve()
        print test.nodes
        for node in self.nodes:
            node.update()
            node.neighbors = []
        for i, node in enumerate(self.sources):
            gui.update_sent(i, "Sent: {}".format(node.sent))
            stats[node.team].sent = node.sent
        for i, node in enumerate(self.sinks):
            gui.update_score(i, "Score: {}".format(node.score))
            if node.updated:
                stats[node.team].numhops.append(node.lasthops)
                node.updated = False
        for i in interference:
            gui.update_inter(i, "Interference{} = {}".format(i, interference[i]))
            stats[i].interference.append(interference[i])
            stats[i].ratio.append(len(stats[i].numhops)/stats[i].sent)
        root.update()

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
    stats[1] = Stats()
    stats[2] = Stats()
    gui.add_team(1)
    test.addSource((0,0), "test", 1)
    test.addHPNode((0,1), 1)
    test.addHPNode((0,2), 1)
    test.addHPNode((0,3), 1)
    test.addHPNode((0,4), 1)
    test.addSink((0,5), "test", 1)


    gui.add_team(2)
    test.addSource((3,0), "test", 2)
    test.addHPNode((3,1), 2)
    test.addHPNode((3,2), 2)
    test.addHPNode((3,3), 2)
    test.addHPNode((3,4), 2)
    test.addSink((3,5), "test", 2)

    print test
    loop()


def teamTestClose():
    stats[1] = Stats()
    stats[2] = Stats()
    stats[3] = Stats()
    gui.add_team(1)
    test.addSource((0,0), "test", 1)
    test.addHPNode((1,1), 1)
    test.addHPNode((1,2), 1)
    test.addHPNode((1,3), 1)
    test.addHPNode((1,4), 1)
    test.addSink((0,5), "test", 1)


    gui.add_team(2)
    test.addSource((3,0), "test", 2)
    test.addHPNode((2,1), 2)
    test.addHPNode((2,2), 2)
    test.addHPNode((2,3), 2)
    test.addHPNode((2,4), 2)
    test.addSink((3,5), "test", 2)

    gui.add_team(3)
    test.addSource((5,0), "test", 3)
    test.addHPNode((5,1), 3)
    test.addHPNode((5,2), 3)
    test.addHPNode((5,3), 3)
    test.addHPNode((5,4), 3)
    test.addSink((5,5), "test", 3)


    print test
    loop()




def smartteamTest():
    gui.add_team(2)
    stats[2] = Stats()
    test.addSource((5,5), "test", 2)
    test.addNoiseNode((3, 3))
    test.addSmartNode((1, 1), 2)
    test.addSmartNode((4, 4), 2)
    test.addSmartNode((4, 3), 2)
    test.addSmartNode((3, 4), 2)
    test.addSmartNode((2, 4), 2)
    test.addSmartNode((4, 2), 2)
    test.addSmartNode((2, 2), 2)
    test.addSmartNode((2, 3), 2)
    test.addSink((3,1), "test", 2)
    print test
    loop()


def plot():
    import matplotlib.pyplot as plt
    for x in stats:
        plt.figure()
        plt.plot(stats[x].numhops)
        plt.title("number of hops per packet at sink")
        plt.savefig("hops{}.png".format(x))
        plt.figure()
        plt.plot(stats[x].interference)
        plt.title("total amount of interference at each timestep")
        plt.savefig("interf{}.png".format(x))
        plt.figure()
        plt.plot(stats[x].ratio)
        plt.title("throughput vs time")
        plt.savefig("ratio{}.png".format(x))



#test.loadConfig("simpleTest.fld")
root.update()
try:
    #defaultTest()
    #teamTest()
    teamTestClose()
    #smartteamTest()
finally:
    plot()
