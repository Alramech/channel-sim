import random
import string
from collections import defaultdict
jumble=lambda*p:[x[0]+t for x,y in p,p[::-1]for t in x and jumble(x[1:],y)]or['']
interference = defaultdict(int)

class Packet:
    def __init__(self, token, origin, channel = 0, numhops = 0, team = 0, type = "MSG"):
        self.token = token
        self.origin = origin
        self.channel = channel
        self.numhops = numhops
        self.team = team
        self.type = type

    def copy(self):
        return Packet(self.token, self.origin, self.channel, self.numhops, self.team, self.type)

    def __repr__(self):
        return "{}: {}, hops {}".format(self.type, self.token, self.numhops)
class Node:
    def __init__(self, pos, ntype):
        self.pos = pos
        self.type = ntype
        self.status = "REC"
        self.neighbors = []
        self.readbuffer = [None] * 16
        self.sendbuffer = [None] * 16
        self.ackbufffer = [None] * 16
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
            token.type = "INTERFERENCE"
            print "Receiving {} from {} at {} caused interference to {} at {}".format(
                token.token, token.origin.type, token.origin.pos, self.type, self.pos)
            self.readbuffer[channel] = token

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

    def __init__(self, pos, token, channel = 0, team = 0):
        Node.__init__(self, pos, "SOURCE")
        self.token = token
        self.status = "SEND"
        self.nextStatus = "SEND"
        self.cooldown = 0
        self.channel = channel
        self.team = team
        self.sent = 0

    def send(self, msg):
        if (self.cooldown > 0):
            self.cooldown -= 1
            return
        self.cooldown = 10
        num = len(self.neighbors)
        for neighbor in self.neighbors:
            if (neighbor.status == "REC"):
                token =  Packet(self.token, self, self.channel, team = self.team)
                neighbor.addToReadBuffer(token, self.channel)
                print "Sending {} to {} at {} on channel {}".format(self.token, neighbor.type, neighbor.pos, self.channel)
                break
        self.sent += 1

class SinkNode(Node):
    def __init__(self, pos, token, team = 0):
        Node.__init__(self, pos, "SINK")
        self.token = token
        self.status = "REC"
        self.score = 0
        self.team = team

    def recieve(self):
        for i, item in enumerate(self.readbuffer):
            if item != None and item.token == self.token and item.team == self.team:
                item.numhops += 1
                item.origin.readbuffer[(i+1)%16] = Packet(self.token, self, i, type = "ACK")
                self.score += 1
                print "Delivered {} to sink, score = {}".format(self.token, self.score)
            self.readbuffer[i] = None
"""
class SmartNode(Node):
    def __init__(self, pos, team = 1):
        Node.__init__(self, pos, "Smart")
        num = random.random()
        self.team = team
        if num < 0.4:
            self.status = "SEND"

    # method to determine which channel to send for a particular neighbor
    # in this particular case, we won't care about noise, but this may
    # be problematic
    def channel_to_send_neighbor(self, neighbor):
        ind = None
        if neighbor.status == "REC":
            ind = 0
            while ind < 16 and (neighbor.readbuffer[ind] == None or neighbor.readbuffer[ind].origin == None):
                ind += 1
            if neighbor.readbuffer[ind] == None or neighbor.readbuffer[ind].origin == None:
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
                    buffer_cont = neighbor.readbuffer[ind]
                    if buffer_cont != None:
                        if buffer_cont[1] != None:
                            channel_traffic += 1
                        else:
                            # if there's noise only, just increment by 0.5
                            channel_traffic += 0.5
                else:
                    buffer_cont = neighbor.sendbuffer[ind]
                    if buffer_cont != None:
                        channel_traffic += 1
            if channel_traffic < smallest_num:
                smallest_num = channel_traffic
                smallest_num_index = ind

        return smallest_num_index


    def send(self, msg = None):
        # first determine which channel is least traffic congested
        channel = self.channel_to_send()

        for i, v in enumerate(self.sendbuffer):
            if v != None:
                self.sendbuffer[i] = None
                msg = v
                break
        if msg == None:
            return
            msg = sendbuffer[0]

        # now set send buffer to the desired msg
        self.sendbuffer[channel] = msg
        for neighbor in self.neighbors:
            if neighbor.status == "REC":
                if neighbor.readbuffer[channel] != None:
                    # TODO: what do we do here? just give up or try to send on another channel
                    # for this specific neighbor?
                    channel = self.channel_to_send_neighbor(neighbor)
                buffer_contents = neighbor.readbuffer[channel]
                if buffer_contents != None and buffer_contents[1] == None:
                    # There's noise, so we still add it, but its jumbled
                    possibilities = jumble(buffer_contents[0], msg)
                    jumble_choice = possibilities[random.randint(0, possibilities.length)]
                    neighbor.readbuffer[channel] = (jumble_choice, self)
                    print "{} at {} sending {} to {} at {} on channel {}".format(self.type, self.pos, jumble_choice, neighbor.type, neighbor.pos, channel)
                elif buffer_contents == None:
                    # no noise or other nodes trying to communicate
                    neighbor.readbuffer[channel] = (msg, self)
                    print "{} at {} sending {} to {} at {} on channel {}".format(self.type, self.pos, msg, neighbor.type, neighbor.pos, channel)
        # Not sure about this?
        self.nextStatus = "REC"

    # in this case, dst is neighbor
    def send_neighbor(self, msg, dst):
        if dst.status == "SEND":
            return
        channel = channel_to_send_neighbor(dst)
        buffer_contents = dst.readbuffer[channel]
        if buffer_contents != None and buffer_contents[1] == None:
            # There's noise, so we still add it, but its jumbled
            possibilities = jumble(buffer_contents[0], msg)
            jumble_choice = possibilities[random.randint(0, possibilities.length)]
            neighbor.readbuffer[channel] = (jumble_choice, self)
            print "{} at {} sending {} to {} at {} on channel {}".format(self.type, self.pos, jumble_choice, neighbor.type, neighbor.pos, channel)
        elif buffer_contents == None:
            # no noise or other nodes trying to communicate
            neighbor.readbuffer[channel] = (msg, self)
            print "{} at {} sending {} to {} at {} on channel {}".format(self.type, self.pos, msg, neighbor.type, neighbor.pos, channel)
        self.nextStatus = "REC"

    def recieve(self):
        # listen to all channels
        for i, item in enumerate(self.readbuffer):
            if item == None:
                continue

            if item == "INTERFERENCE":
                continue
            print item
            if item[0] == "ACK" or item[0] == "Hi":
                continue
            if item[1]:
                print "{} at {} recieved {} from {} at {} on channel {}".format(self.type, self.pos, item[0], item[1].type, item[1].pos, i)
                item[1].sendbuffer[i] = item[0]
            else:
                print "{} at {} recieved {} on channel {}".format(self.type, self.pos, item[0], i)

            self.readbuffer[i] = None

        # Not sure about this?
        if not all(x is None for x in self.sendbuffer):
            self.nextStatus = "SEND"
"""
class NoiseNode(Node):
    def __init__(self, pos):
        Node.__init__(self, pos, "Noise")
        self.status = "SEND"
        self.team = -1

    def send(self, msg):
        # generate gaussian noise (alphanumeric string) and add at end
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        noise = ''.join(random.choice(chars) for i in range(32))

        # choose a random channel to send on
        rand_channel = random.randint(0, 16)
        for neighbor in self.neighbors:
            if neighbor.status == "REC":
                # currently nothing there
                neighbor.addToBuffer(Packet(noise, None, rand_channel), rand_channel)
                """
                if neighbor.readbuffer[rand_channel] == None:
                    neighbor.readbuffer[rand_channel] = 
                else:
                    curr_msg, curr_sender = neighbor.readbuffer[rand_channel]
                    neighbor.readbuffer[rand_channel] = (curr_msg + noise, curr_sender)
                """
        print "Added noise {} at {} on channel {}".format(noise, self.pos, rand_channel)

    # Noise nodes don't need to receive anything, only generate noise
    def recieve(self):
        pass

class HotPotatoNode(Node):
    def __init__(self, pos, team = 1):
        Node.__init__(self, pos, "HP")
        self.team = team

    def send(self, msg):
        recneighbor = [neg for neg in self.neighbors if neg.status == "REC"]
        num = len(recneighbor)
        if num == 0:
            return
        for i, smsg in enumerate(self.sendbuffer):
            if smsg == None or smsg.team != self.team:
                continue
            randNeighbor = recneighbor[random.randint(0, num-1)]
            token = smsg.copy()
            print "{} at {} sending {} to {} at {}".format(self.type, self.pos, smsg, randNeighbor.type, randNeighbor.pos)
            randNeighbor.addToReadBuffer(token, 0)
        self.nextStatus = "REC"

    def recieve(self):
        for i, item in enumerate(self.readbuffer):
            if item != None and item.type == "ACK":
                self.sendbuffer[item.channel] = None
                print "{} at {} recieved ack for {} on channel {} from {}".format(self.type, self.pos, item.token, item.channel, item.origin.pos)
                self.readbuffer[i] = None
        for i, item in enumerate(self.readbuffer):
            if item == None:
                self.readbuffer[i] = None
                continue
            if item.type == "INTERFERENCE":
                self.readbuffer[i] = None
                interference[self.team] += 1
                continue

            if item.origin == None:
                pass
            else:
                print "{} at {} recieved {} from {} at {} on channel {}".format(self.type, self.pos, item.token, item.origin.type, item.origin.pos, i)
                ackchannel = (i+1) % 16
                item.origin.readbuffer[ackchannel] = Packet(item.token, self, channel = i, type ="ACK")
                sendmsg = item.copy()
                sendmsg.origin = self
                sendmsg.numhops += 1
                self.sendbuffer[i] = sendmsg
            self.readbuffer[i] = None
        if not all(x is None for x in self.sendbuffer):
            self.nextStatus = "SEND"
