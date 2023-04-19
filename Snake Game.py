#! python3

from tkinter import *
import random


root = Tk()

turns = []
count = []
length = 0
segment = -1
moved = False

class PlayArea():
        def __init__(self, size, cells):
            self.size = size
            self.cell = cells
            self.canvas = Canvas(root, width = self.size, height = self.size, bg = "black")
            self.CreateApple()


        def CreateArea(self):
            self.canvas.pack()

            for i in range(self.cell):
                self.canvas.create_line(i*self.spacing,0, i*self.spacing, self.size, fill = "gray")

            for i in range(self.cell):
                self.canvas.create_line(0, i*self.spacing, self.size, i*self.spacing, fill = "gray")

            return self.canvas, self.size, self.cell

        def CreateApple(self):
                self.spacing = self.size/self.cell
                x = (random.randint(2, self.cell-2) * self.spacing) + 1
                y = x
                size = self.spacing-2

                self.canvas.create_rectangle(x, y, x + size, y + size, fill = "red", tag = "apple")
                self.canvas.tag_lower("apple")

        


                
class Snake():
    def __init__(self, canvas, size, cell, HLocation = 3, VLocation = 3, HMove = 1, VMove = 0, ):
        self.HMove = HMove
        self.VMove = VMove
        self.canvas = canvas
        self.size = size
        self.cell = cell
        self.speed = speed
        self.spacing = self.size/self.cell
        self.HLocation = HLocation
        self.VLocation = VLocation
  
        
    def CreateSnake(self):
        global length, segment
        size = (self.spacing) - 2
        HStart = self.HLocation * self.spacing + 1
        VStart = self.VLocation * self.spacing + 1
        
        length += 1
        segment += 1
        
        self.body = self.canvas.create_rectangle(HStart, VStart, size + HStart, size + VStart, fill = "white", tag = "segment"+str(segment))
        
    def UpdateLocation(self):
        if self.HMove != 0:
            self.HLocation += self.HMove

        if self.VMove != 0:   
            self.VLocation += self.VMove      
        
    def Move(self):
        global speed
        self.UpdateLocation()
        HJump = self.HMove * self.spacing
        VJump = self.VMove * self.spacing
        
        if self.HLocation > self.cell:
            HJump = self.size * -1
            self.HLocation = 0

        elif self.HLocation < 0:
            HJump = self.size
            self.HLocation = self.cell

        if self.VLocation > self.cell:
            VJump = self.size * -1
            self.VLocation = 0

        elif self.VLocation < 0:
            VJump = self.size
            self.VLocation = self.cell
            
        self.canvas.move(self.body, HJump, VJump)
        self.speed = speed
        self.canvas.after(self.speed, self.Move)  
        
class Head(Snake):
    def __init__(self, canvas, size, cell):
        Snake.__init__(self, canvas, size, cell)
        
        self.canvas.focus_set()
        self.canvas.bind("<w>", lambda D: self.Arrow("up"))
        self.canvas.bind("<a>", lambda D: self.Arrow("left"))
        self.canvas.bind("<s>", lambda D: self.Arrow("down"))
        self.canvas.bind("<d>", lambda D: self.Arrow("right"))
        
    def CreateSnake(self):
            Snake.CreateSnake(self)
            Body(self.canvas, self.size, self.cell,2, 3)
            Body(self.canvas, self.size, self.cell,1, 3)
                
            
    def Arrow(self, D):
        global turns, moved
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
        if  abs(dif) == 1 and moved == True:
            self.VMove = VMove
            self.HMove = HMove

            moved = False


            turns.append([self.canvas.coords(self.body), HMove, VMove])

        

    def CheckApple(self):
            global speed
            applecoords = self.canvas.coords("apple")
            mycoords = self.canvas.coords(self.body)
            
            if applecoords == mycoords:
                    self.canvas.delete("apple")
                    PlayArea.CreateApple(self)
                    
                    if speed > 60:
                            speed = speed - 10
                            
                    HLocation = self.HLocation
                    VLocation = self.VLocation

                    if self.HMove != 0:
                            HLocation = HLocation


                    elif self.VMove != 0:
                            VLocation = VLocation
                            
                    self.canvas.move(self.body, self.HMove*self.spacing, self.VMove*self.spacing)
                    self.HLocation += self.HMove
                    self.VLocation += self.VMove
                    
                    Body(self.canvas, self.size, self.cell, HLocation, VLocation, self.HMove, self.VMove)

    def RemoveTurn(self):
            mycoords = self.canvas.coords(self.body)
            for i in range(len(turns)):
                    if mycoords == turns[i][0]:
                            turns.remove(turns[i])
                            break
                    
                    
    def Move(self):
            global moved
            Head.CheckApple()
            Snake.Move(self)
            Head.RemoveTurn()
            moved = True
            Head.Collide()

    def Collide(self):
            mycoords = self.canvas.coords(self.body)
            for i in range(1, length-2):
                    othercoords = self.canvas.coords("segment"+str(i))
                    if mycoords == othercoords:
                            self.canvas.destroy()
                            LoseLabel = Label(root, text = "You Lost!")
                            LoseLabel.pack()
                    
            
class Body(Snake):
        def __init__(self, canvas, size, cell, HLocation, VLocation, HMove = 1, VMove = 0):
                Snake.__init__(self, canvas, size, cell, HLocation, VLocation, HMove, VMove)
                global length, segment
                size = (self.spacing) - 2
                HStart = self.HLocation * self.spacing + 1
                VStart = self.VLocation * self.spacing + 1

                length += 1
                segment += 1
                
                self.body = self.canvas.create_rectangle(HStart, VStart, size + HStart, size + VStart, fill = "white", tag = "segment"+str(segment))

                self.Move()
                
        def NextMove(self):
                global turns, length
                mycoords = self.canvas.coords(self.body)
                
                for item in turns:
                        if mycoords == item[0]:
                                self.HMove = item[1]
                                self.VMove = item[2]
                           

                                        
        def Move(self):
                self.NextMove()
                Snake.Move(self)
                
                
                
               

SnakeArea = PlayArea(400, 25)
speed = 200
canvas, size, cell = SnakeArea.CreateArea()

Head = Head(canvas, size, cell)
Head.CreateSnake()

Head.Move()



        
