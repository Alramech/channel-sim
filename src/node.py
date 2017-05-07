import random

class Node:
    def __init__(self, pos, ntype):
        self.pos = pos
        self.type = ntype
        self.status = "REC"
        self.neighbors = []
        self.readbuffer = [None] * 16
        self.sendbuffer = [None] * 16
        self.nextStatus = "REC"
        self.team = 0

    def send(self, msg):
        pass

    def recieve(self):
        pass

    def update(self):
        self.status = self.nextStatus

    def addToReadBuffer(self, token, channel):
        if self.readbuffer[channel] == None:
            self.readbuffer[channel] = token
        else:
            self.readbuffer[channel] = "INTERFERENCE"

    def getMessages(self):
        msgs = []
        for msg in self.readbuffer:
            if msg != None:
                msgs.append(msg)
        return msgs
    def __repr__(self):
        return "{} at {} in state {} \n read {}\n send {}\n".format(
            self.type, self.pos, self.status, self.readbuffer, self.sendbuffer)

class SourceNode(Node):

    def __init__(self, pos, token, channel = 0):
        Node.__init__(self, pos, "SOURCE")
        self.token = token
        self.status = "SEND"
        self.nextStatus = "SEND"
        self.cooldown = 0
        self.channel = channel

    def send(self, msg):
        if (self.cooldown > 0):
            self.cooldown -= 1
            return
        self.cooldown = 10
        num = len(self.neighbors)
        for neighbor in self.neighbors:
            if (neighbor.status == "REC"):
                token =  (self.token, self)
                neighbor.addToReadBuffer(token, self.channel)
                print "Sending {} to {} at {} on channel {}".format(self.token, neighbor.type, neighbor.pos, self.channel)
                break

class SinkNode(Node):
    def __init__(self, pos, token):
        Node.__init__(self, pos, "SINK")
        self.token = token
        self.status = "REC"
        self.score = 0

    def recieve(self):
        for i, item in enumerate(self.readbuffer):
            if item != None and item[0] == self.token:
                item[1].readbuffer[i] = ("ACK", self.token, i)
                self.score += 1
                print "Delivered {} to sink, score = {}".format(self.token, self.score)
            self.readbuffer[i] = None

class HotPotatoNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos, "HP")

    def send(self, msg):
        num = len(self.neighbors)
        for smsg in self.sendbuffer:
            if smsg == None:
                continue
            for neighbor in self.neighbors:
                randNeighbor = self.neighbors[random.randint(0, num-1)]
                if randNeighbor.status == "REC":
                    token = (smsg, self)
                    randNeighbor.addToReadBuffer(token, 0)
                    print "{} at {} sending {} to {} at {}".format(self.type, self.pos, smsg, randNeighbor.type, randNeighbor.pos)
                    break
        self.nextStatus = "REC"

    def recieve(self):
        for i, item in enumerate(self.readbuffer):
            if item == None or item == "INTERFERENCE":
                self.readbuffer[i] = None
                continue
            if item[0] == "ACK":
                self.sendbuffer[item[2]] = None
                print "{} at {} recieved ack for {} on channel".format(self.type, self.pos, item[1], item[2])
            else:
                print item[1]
                item[1].readbuffer[i] = ("ACK", item[0], i)
                self.sendbuffer[i] = (item[0])
                print "{} at {} recieved {} from {} at {} on channel {}".format(self.type, self.pos, item[0], item[1].type, item[1].pos, i)
            self.readbuffer[i] = None
        if not all(x is None for x in self.sendbuffer):
            self.nextStatus = "SEND"
