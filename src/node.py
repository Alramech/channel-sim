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
                neighbor.readbuffer[self.channel] = (self.token, self)
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

class SmartNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos, "Smart")

    # method to determine which channel to send for a particular neighbor
    def channel_to_send_neighbor(self, neighbor):
        ind = None
        if neighbor.status == "REC":
            ind = 0
            while ind < neighbor.readbuffer.length and neighbor.readbuffer[ind] == None:
                ind += 1
            if ind == neighbor.readbuffer.length:
                ind = None

        return ind

    # method to determine which channel to send in general (traffic)
    def channel_to_send(self):
        ind = None
        smallest_num = float('inf')
        smallest_num_index = -1
        for ind in range(16):
            channel_traffic = 0
            for neighbor in self.neighbors:
                if neighbor.status == "REC":
                    if neighbor.readbuffer[ind] != None:
                        channel_traffic += 1
                else:
                    if neighbor.sendbuffer[ind] != None:
                        channel_traffic += 1
            if channel_traffic < smallest_num:
                smallest_num = channel_traffic
                smallest_num_index = ind

        return smallest_num_index


    def send(self, msg):
        # first determine which channel is least traffic congested
        channel = self.channel_to_send()

        # now set send buffer to the desired msg
        self.sendbuffer[channel] = msg
        for neighbor in self.neighbors:
            if neighbor.status == "REC":
                if neighbor.readbuffer[channel] != None:
                    # TODO: what do we do here? just give up or try to send on another channel
                    # for this specific neighbor?
                    channel = channel_to_send_neighbor(neighbor)
                neighbor.readbuffer[channel] = (msg, self)
                print "{} at {} sending {} to {} at {} on channel {}".format(self.type, self.pos, msg, neighbor.type, neighbor.pos, channel)
        
        # Not sure about this?
        self.nextStatus = "REC"

    # in this case, dst is neighbor
    def send(self, msg, dst):
        channel = channel_to_send_neighbor(dst)
        neighbor.readbuffer[channel] = (msg, self)
        print "{} at {} sending {} to {} at {} on channel {}".format(self.type, self.pos, msg, neighbor.type, neighbor.pos, channel)
        self.nextStatus = "REC"

    def recieve(self):
        # listen to all channels
        for i, item in enumerate(self.readbuffer):
            if item == None:
                continue
            print "{} at {} recieved {} from {} at {} on channel {}".format(self.type, self.pos, item[0], item[1].type, item[1].pos, i)
            self.readbuffer[i] = None
            item[1].sendbuffer[i] = None

        # Not sure about this?
        if not all(x is None for x in self.sendbuffer):
            self.nextStatus = "SEND"


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
                    randNeighbor.readbuffer[0] = (smsg, self)
                    print "{} at {} sending {} to {} at {}".format(self.type, self.pos, smsg, randNeighbor.type, randNeighbor.pos)
                    break
        self.nextStatus = "REC"

    def recieve(self):
        for i, item in enumerate(self.readbuffer):
            if item == None:
                continue
            if item[0] == "ACK":
                self.sendbuffer[item[2]] = None
                print "{} at {} recieved ack for {} on channel".format(self.type, self.pos, item[1], item[2])
            else:
                item[1].readbuffer[i] = ("ACK", item[0], i)
                self.sendbuffer[i] = (item[0])
                print "{} at {} recieved {} from {} at {} on channel {}".format(self.type, self.pos, item[0], item[1].type, item[1].pos, i)
            self.readbuffer[i] = None
        if not all(x is None for x in self.sendbuffer):
            self.nextStatus = "SEND"
