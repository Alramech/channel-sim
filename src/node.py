import random

class Node:
    def __init__(self, pos, ntype):
        self.pos = pos
        self.type = ntype
        self.status = "REC"
        self.neighbors = []
        self.readbuffer = []
        self.sendbuffer = []
        self.nextStatus = "REC"
        self.team = 0

    def send(self, msg):
        pass

    def recieve(self):
        pass

    def update(self):
        self.status = self.nextStatus

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
                neighbor.readbuffer.append( (self.token, self) )
                print "Sending {} to {} at {}".format(self.token, neighbor.type, neighbor.pos)
                break

class SinkNode(Node):
    def __init__(self, pos, token):
        Node.__init__(self, pos, "SINK")
        self.token = token
        self.status = "REC"
        self.score = 0

    def recieve(self):
        for item in self.readbuffer:
            if item[0] == self.token:
                item[1].readbuffer.append(("ACK", self.token))
                self.score += 1
        self.readbuffer = []

class HotPotatoNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos, "HP")

    def send(self, msg):
        num = len(self.neighbors)
        for smsg in self.sendbuffer:
            for neighbor in self.neighbors:
                randNeighbor = self.neighbors[random.randint(0, num-1)]
                if randNeighbor.status == "REC":
                    randNeighbor.readbuffer.append((smsg, self))
                    print "{} at {} sending {} to {} at {}".format(self.type, self.pos, smsg, randNeighbor.type, randNeighbor.pos)
                    break
        self.nextStatus = "REC"

    def recieve(self):
        for item in self.readbuffer:
            if item[0] == "ACK":
                self.sendbuffer.remove(item[1])
                print "{} at {} recieved ack for {}".format(self.type, self.pos, item[1])
            else:
                item[1].readbuffer.append(("ACK", item[0]))
                self.sendbuffer.append(item[0])
                print "{} at {} recieved {} from {} at {}".format(self.type, self.pos, item[0], item[1].type, item[1].pos)
        self.readbuffer = []
        if len(self.sendbuffer) > 0:
            self.nextStatus = "SEND"
