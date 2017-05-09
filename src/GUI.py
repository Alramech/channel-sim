from tkinter import *
from collections import defaultdict

class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Netsym")
        canvas_width = 800
        canvas_height = 400

        self.w = Canvas(master, width = canvas_width, height = canvas_height)
        self.w.pack()

        self.scores = []
        self.sent = []
        self.packets = defaultdict(list)
        self.w.create_rectangle(0, 0, 400, 400, fill="#FFFFFF")
        self.num_scores = 0
        self.num_sent = 0
        self.num_teams = 0
        self.stats = []
        self.teams = {}


    def add_node(self, pos, color = "#000000"):
        x = pos[0]*20
        y = pos[1]*20

        self.w.create_rectangle(x+5, y+5, x+15, y+15, fill=color)

    def add_line(self, pos, pos2, color = "#000000"):
        x1 = pos[0]*20
        y1 = pos[1]*20

        x2 = pos2[0]*20
        y2 = pos2[1]*20
        self.w.create_line(x1+10, y1+10, x2+10, y2+10, fill=color)

    def add_score(self):
        x1 = 700
        y1 = 100 + self.num_scores * 10
        self.num_scores += 1
        sc = self.w.create_text(x1+10, y1+10, text = "Score1 = ")
        self.scores.append(sc)

    def update_score(self, i, txt):
        self.w.itemconfig(self.scores[i], text=txt)

    def add_sent(self):
        x1 = 480
        y1 = 100 + self.num_scores * 10
        self.num_sent += 1
        sc = self.w.create_text(x1+10, y1+10, text = "Sent:")
        self.sent.append(sc)

    def update_sent(self, i, txt):
        self.w.itemconfig(self.sent[i], text=txt)



    def add_team(self, i):
        x = 420
        y = 100 + self.num_teams * 10
        self.w.create_text(x+10, y+10, text = "Team {}: ".format(i))


        x1 = 570
        y1 = 100 + self.num_teams * 10
        self.num_teams += 1
        sc = self.w.create_text(x1+10, y1+10, text = "Interference = 0")
        self.teams[i] = ([sc])

    def update_inter(self, i, txt):
        if i in self.teams:
            self.w.itemconfig(self.teams[i][0], text=txt)


    def update_packets(self, pos, buf, color = "green"):
        x = pos[0]*20
        y = pos[1]*20
        old = self.packets[(x,y)]
        for rec in old:
            self.w.delete(rec)
        self.packets[(x,y)] = []
        for i, val in enumerate(buf):
            if val == None or val == "INTERFERENCE":
                #self.w.create_line(x+5+i, y+2, x+5+i+1, y+2, fill="white")
                self.w.create_rectangle(x+5, y+10, x+10, y+15, fill="white")
            else:
                #self.w.create_line(x+5+i, y+2, x+5+i+1, y+2, fill=color)
                if (val.type != "ACK"):
                    self.w.create_rectangle(x+5, y+10, x+10, y+15, fill=color)
                    break



root = Tk()
gui = GUI(root)

