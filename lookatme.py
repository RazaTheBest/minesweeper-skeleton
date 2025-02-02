import tkinter as tk
from tkinter import font as tkFont
import random


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.titlefont = tkFont.Font(family="Arial", size=20, slant="italic")
        self.buttonFont = tkFont.Font(family="Arial", size=18)
        self.label = tk.Label(self, text="Minesweeper", font=self.titlefont)
        self.label.grid(row=0, column=1)
        self.goButton = tk.Button(self, text="    Go!    ", command=self.go, bg="green", fg="white")
        self.goButton.grid(row=0, column=0)
        self.buttongrid = tk.Frame(self)
        self.buttongrid.grid(row=2, column=0, sticky="NSEW", columnspan=2)
        self.buttons = []
        self.flagImage = tk.PhotoImage(file="flag.gif")
        self.mineImage = tk.PhotoImage(file="mine.gif")
        self.nomineImage = tk.PhotoImage(file="nomine.gif")
        buttonNum = 0
        for rownum in range(10):
            for columnnum in range(10):
                self.buttons.append(tk.Button(self.buttongrid, text=" ", font=self.titlefont))
                self.buttons[buttonNum].bind("<Button-1>", lambda event, x=buttonNum: self.buttonLeftClicked(event, x))
                self.buttons[buttonNum].bind("<Button-3>", lambda event, x=buttonNum: self.buttonRightClicked(event, x))
                self.buttons[buttonNum].config(height=50, width=50)
                self.buttons[-1].grid(row=rownum, column=columnnum, sticky="NSEW")
                self.buttongrid.rowconfigure(rownum, weight=1)
                self.buttongrid.columnconfigure(columnnum, weight=1)
                buttonNum += 1
        self.rowconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)
        self.go()

    def buttonLeftClicked(self, event, pos):
        if self.gameOn:
            print("Button", pos, " was left clicked")
            if self.minepositions[pos] == 1:
                self.dead()
            else:
                self.floodfill(pos)

        # if it's not a mine, it changes to show the number of mines in neighbouring cells (see getNoMines)
        # if there are no neighbouring mines (so it's blank) it flood-fills to reveal all contiguous blank cells
    

    def buttonRightClicked(self, event, pos):
        # when right clicked, a mine will either show a flag or hide the flag
        if self.buttons[pos].cget("image") == "pyimage1":
            self.buttons[pos].config(image="")
        else:
            self.buttons[pos].config(image=self.flagImage)
        

    def placeMines(self):
        self.minepositions = [0 for x in range(100)]
        # self.minepositions is a 100-slot array containing 0 for blank cells and 1 for mines
        # 20 mines should be placed randomly
        
        minecount = 0
        while minecount < 20:
            num = random.randint(0,99)
            if self.minepositions[num] == 0:
                self.minepositions[num] = 1
                #self.buttons[num].config(text="X")
                minecount+=1


    def getNoMines(self, pos):
        numberMines = 0
        # this checks the neighbouring cells of postion pos and counts the number of mines
        # it returns the number
        col = pos % 10
        row = pos // 10
        for rowdiff,coldiff in [[-1,-1],[-1,0],[-1,1], [0,-1],[0,1],[1,-1], [1,0],[1,1]]:
            cellRow = row + rowdiff
            cellCol = col + coldiff
            if 0<=cellRow<10 and 0 <= cellCol < 10:
                numberMines += self.minepositions[cellRow*10+cellCol]
        #for diff in [-11,-10,-9,-1,1,9,10,11]:
            #cell = pos + diff
            #cellRow = cell // 10
            #cellCol = col%10
        #self.buttons[pos].config(text=numberMines)
        return numberMines

    def dead(self):
        self.gameOn = False
        # This changes all the cells to red, reveals the mines and ends the game
        for pos in range(100):
            if self.minepositions[pos] == 1:
                # To change the image on a button to a mine, use this:
                self.buttons[pos].config(image=self.mineImage)
            # To change the colour and style of button:
            self.buttons[pos].config(state="normal", bg="red", relief="raised")

    def floodfill(self, pos):
        # This reveals all the contiguous blank spaces in a flood-fill manner.
        # so all the blank cells are revealed, and a 'border' of mine numbers around the area are also revealed

        # To make a button appear flat:
        # self.buttons[pos].config(image="", state="disabled", relief="flat", bg="lightblue")

        q = [pos]
        visited=[ ]

        while len(q) >0:
            # pop the first item from the queue
            thispos = q.pop(0)
            visited.append(thispos)
            # find out how many neighbouring mines it has
            mines = self.getNoMines(thispos)
            # if it's a number > 0: put the number on this button
            if mines > 0:
                self.buttons[thispos].config(text=mines)
            # if its zero, add all of its neighbors into the queue
            else:
                self.buttons[thispos].config(image="", state="disabled", relief="flat", bg="lightblue")
                col = thispos % 10
                row = thispos // 10
                for rowdiff,coldiff in [[-1,-1], [-1,0],[-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1] ]:
                    cellRow = row + rowdiff
                    cellCol = col + coldiff
                    cellPos = cellRow*10 + cellCol
                    # only add to the queue if it's not already visited and it fits in the grid
                    if cellPos not in visited and 0<=cellRow<10 and 0 <= cellCol < 10:
                        q.append(cellPos)


    def go(self):
        self.placeMines()
        #after calling placeMines, this puts all the buttons back to their blank starting style
        for button in self.buttons:
            button.config(state="normal", relief="raised", bg="lightgrey", image="",text="")
        self.gameOn = True


mine = App()
mine.geometry("800x800+200+200")
mine.title("Minesweeper")
mine.mainloop()
