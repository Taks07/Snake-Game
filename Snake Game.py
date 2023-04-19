from tkinter import *
import random

root = Tk()

class Body:
    def __init__(self, canvas, xpos, ypos, spacing, segtag, HMove = 1, VMove = 0):
        self.canvas = canvas
        self.spacing = spacing

        self.HMove = HMove
        self.VMove = VMove

        self.canvas.create_rectangle((spacing * xpos) + 2, (spacing * ypos) + 2, (spacing * xpos) + spacing - 2, (spacing * ypos) + spacing - 2, fill = "gray", tag = segtag)
        self.canvas.tag_lower(segtag)

class Head(Body):
    def __init__(self, canvas, xpos, ypos, spacing, segtag):
        Body.__init__(self, canvas, xpos, ypos, spacing, segtag)
        self.canvas.itemconfig(segtag, fill = "white")

        self.turns = []
        self.moved = False

        self.canvas.focus_set()
        self.canvas.bind("<w>", lambda D: self.Arrow("up"))
        self.canvas.bind("<a>", lambda D: self.Arrow("left"))
        self.canvas.bind("<s>", lambda D: self.Arrow("down"))
        self.canvas.bind("<d>", lambda D: self.Arrow("right"))


    def Arrow(self, D):
        VMove = self.VMove
        HMove = self.HMove
        
        if D == "up":
            HMove = 0
            VMove -= 1
            
        elif D == "left":
            HMove -=1
            VMove = 0

        elif D == "down":
            HMove = 0
            VMove += 1

        else:
            HMove += 1
            VMove = 0

        dif = HMove - VMove
        if  abs(dif) == 1 and self.moved == True:
            self.VMove = VMove
            self.HMove = HMove

            self.moved = False

            self.turns.append([self.canvas.coords("seg0"), HMove, VMove])

        
        
class Snake:
    def __init__(self, size, cells, speed):
        self.size = size
        self.cells = cells
        self.speed = speed
        self.canvas = Canvas(root, width = self.size, height = self.size, bg = "black")


        self.spacing = size/cells
        self.segments = [] # 2D array of [Object, Tag] elements
        self.segcount = 0
        self.tag = "seg0"

        self.CreateArea()
     
        self.segments.append([Head(self.canvas, 3, 1, self.spacing, str(self.tag)), str(self.tag)])
        self.UpdateTagging()      

        self.segments.append([Body(self.canvas, 2, 1, self.spacing, str(self.tag)), str(self.tag)])
        self.UpdateTagging()

        self.segments.append([Body(self.canvas, 1, 1, self.spacing, str(self.tag)), str(self.tag)])
        self.UpdateTagging()

        self.CreateApple()
        self.Move()

#Play Area
    def CreateArea(self):
        self.canvas.pack()

        for i in range(self.cells): #Draw horizontal lines
            self.canvas.create_line(0, i * self.spacing, self.size, i * self.spacing, fill = "white")

        for i in range(self.cells): #Draw vertical lines
            self.canvas.create_line(i * self.spacing, 0, i * self.spacing, self.size, fill = "white")
            
    def GameLose(self):
        self.canvas.destroy()
        LoseLabel = Label(root, text = "You lost!")
        
        LoseLabel.pack()

    def CreateApple(self):
        xpos = random.randint(1, self.cells-1) * self.spacing
        ypos = random.randint(1, self.cells-1) * self.spacing

        for i in range(len(self.segments)):
            coord = self.canvas.coords(self.segments[i][1])
            if (xpos + 2) == coord[0] and (ypos+2) == coord[1]:
                self.CreateApple()
                return
        
        self.apple = self.canvas.create_rectangle(xpos + 2, ypos + 2, xpos + self.spacing - 2, ypos + self.spacing - 2, fill = "red", tag = "apple")
        self.canvas.tag_lower("apple")

    
#Snake Itself        
    def Move(self):
        self.turns = self.segments[0][0].turns
        head = self.segments[0]
        size = int(self.canvas["width"])
        
        self.canvas.move(head[1], head[0].HMove * self.spacing, head[0].VMove * self.spacing)
        headcoords = self.canvas.coords("seg0")
        head[0].moved = True

        if headcoords[0] < 0 or headcoords[1] < 0 or headcoords[2] > size or headcoords[3] > size:
            self.GameLose()
            return

        for i in range(1, len(self.segments)):
                       if headcoords == self.canvas.coords(self.segments[i][1]):
                           self.GameLose()
                           return
            

        for i in range(len(self.turns)):
            turn = self.turns[i]
            if self.canvas.coords("seg0") == turn[0]:
                head[0].turns.remove(turn)
                self.turns = head[0].turns

                break

        if headcoords == self.canvas.coords("apple"):
            self.canvas.delete(self.apple)
            self.ExtendSnake()
            self.CreateApple()
                
        for i in range(1, len(self.segments)):
            seg = self.segments[i]
            self.canvas.move(seg[1], seg[0].HMove * self.spacing, seg[0].VMove * self.spacing)

            for turn in self.turns:
                if self.canvas.coords(seg[1]) == turn[0]:
                    seg[0].HMove, seg[0].VMove = turn[1], turn[2]
                
        self.canvas.after(self.speed, self.Move)

    def ExtendSnake(self):
        lastseg = self.segments[-1]
        lastcoords = self.canvas.coords(lastseg[1])

        xpos = ((lastcoords[0]-2)/self.spacing) - lastseg[0].HMove
        ypos = ((lastcoords[1]-2)/self.spacing) - lastseg[0].VMove

        self.segments.append([Body(self.canvas, xpos, ypos, self.spacing, str(self.tag), lastseg[0].HMove, lastseg[0].VMove), str(self.tag)])
        self.UpdateTagging()

        if self.speed > 100:
            self.speed -= 10

        
    def UpdateTagging(self):
        self.segcount += 1
        self.tag = "seg" + str(self.segcount)

if __name__ == "__main__":
    MainSnake = Snake(400, 20, 200)


        
        
        
    
    
