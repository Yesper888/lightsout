"""
Lights Out Puzzle Solver for fewest moves
By Jasper
8/14/17
TODO:
    Add Configuration Tester
    Make an array that stores the discovered data, indexed by effect on bottom row
    Make Output a Solution Matrix
    Add file functionality (and maybe cmd line)
"""

class Board:
    def __init__(self,n,m):
        #Creates grid of n rows by m columns (all off)
        self.data = [m*[False] for i in range(n)]
        self.rows = n
        self.cols = m
        self.solution = [m*[False] for i in range(n)]

    def __str__(self):
        result = ""
        for row in self.data:
            temp = ""
            for cell in row:
                temp+="1" if cell else "0"
            result+=temp+"\n"
        return result

    def switch(self,x,y):
        #Switches cell at (x,y)
        self.data[x][y] = not self.data[x][y]

    def click(self,x,y):
        #Switches current and adjacent cells
        self.solution[x][y] = not self.solution[x][y]
        self.switch(x,y)
        if(x>0): self.switch(x-1,y)
        if(y>0): self.switch(x,y-1)
        if(x<self.rows-1): self.switch(x+1,y)
        if(y<self.cols-1): self.switch(x,y+1)

    def chase(self):
        #Basically clicking all the cells with a light
        #above it, from the top row to the bottom
        for x in range(self.rows-1):
            for y in range(self.cols):
                if(self.data[x][y]): self.click(x+1,y)

    def getBot(self):
        #Return a COPY of the bottom row
        return list(self.data[self.rows-1])

    def clearBot(self):
        #Just a convenient little method for preserving encapsulation
        self.data[self.rows-1] = self.cols*[False]

    def moves(self):
        result=0
        for row in self.solution:
            for cell in row:
                if(cell): result+=1
        return result

    def answer(self):
        result = ""
        for row in self.solution:
            temp = ""
            for cell in row:
                temp+="1" if cell else "0"
            result+=temp+"\n"
        return result

    def copy(self):
        temp = Board(self.rows,self.cols)
        temp.data = [list(x) for x in self.data]
        temp.solution = [list(x) for x in self.solution]
        return temp



def main():
    filename = input("Input File: ")
    with open(filename) as file:
        data = file.readlines()
    rows,cols = tuple(map(int,data[0].split()))
    board = Board(rows,cols)
    for x in range(1,rows+1):
        for y in range(cols):
            if(data[x][y]=="1"):
                board.switch(x-1,y)
                #Don't click here, because it will
                #register in solution matrix
    print(board)
    solutions = [None]*2**cols
    noEffect= []
    #Test Each configuration
    blank = Board(rows,cols)
    curr = [False]*cols
    for i in range(2**cols):
        #click all cells according to curr
        for i in range(cols):
            if(curr[i]): blank.click(0,i)
        blank.chase()
        #store result
        result = blank.getBot()
        slot = 0
        for i in range(cols):
            if(result[i]): slot+=2**i
        if(slot==0):
            noEffect.append(list(curr))
        elif(solutions[slot]==None):
            solutions[slot] = list(curr)
        blank.clearBot()
        #"add 1" to curr (like binary in reverse)
        #For example: [True,False,True] -> [False,True,True]
        for j in range(cols):
            if(curr[j]):
                curr[j] = False
                continue #Just in case
            else:
                curr[j] = True
                break
    #Now that we have solutions we can calculate fewest moves
    #Steps:
    # 1. Chase (while logging all clicks in solution matrix)
    # 2. Look Up effect in solutions
    # 3. Click cells according to ^
    # 4. Chase again
    # 4. Count cells in solution matrix
    # 5. Apply all noEffect configurations
    # 6. Return solution matrix with fewest moves
    board.chase()
    result = board.getBot()
    slot=0
    for i in range(cols):
        if(result[i]): slot+=2**i
    for i,cell in enumerate(solutions[slot]):
        if(cell): board.click(0,i)
    board.chase()
    best = board.moves()
    bestConf = None
    for conf in noEffect:
        copy = board.copy()
        for i in range(cols):
            if(conf[i]): copy.click(0,i)
        copy.chase()
        if(copy.moves()<best):
            best = copy.moves()
            bestConf = list(conf)
    if(bestConf!=None):
        for i in range(cols):
            if(bestConf[i]): board.click(0,i)
        board.chase()
    print("Fewest Moves:",best)
    print(board.answer())
    
main()
