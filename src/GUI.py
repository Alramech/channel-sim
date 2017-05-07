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
        self.packets = defaultdict(list)
        self.w.create_rectangle(0, 0, 400, 400, fill="#FFFFFF")
        self.num_scores = 0


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
                if (val[0] != "ACK"):
                    self.w.create_rectangle(x+5, y+10, x+10, y+15, fill=color)
                    break



root = Tk()
gui = GUI(root)

