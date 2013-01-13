"""
file: myBoard.py
language: python3
author: Joe Ksiazek
description: Definitions of classes representing the game board
             and squares on the board.
"""

class Board:
    __slots__ = ('squares', 'walls')
    
    def __init__(self):
        """Create an empty board"""
        self.squares = dict()
        for x in range(9):
            for y in range(9):
                self.squares[(x,y)] = Square(x, y)
                
        self.walls = []
        
    def addWall(self, r1, c1, r2, c2, playerId=0):
        """Put a wall on the board"""
        NewWall = Wall(r1, c1, r2, c2, playerId)
        self.walls.append(NewWall)
        
        
    def __str__(self):
        return "Board with " + str(len(self.squares)) + " squares"

class Square:
    __slots__ = ( 'x', 'y', 'pawnId', 'neighbors' )

    def __init__(self, x, y, pawnId=0, neighbors=[]):
        """Initialize the square.
        x: x-coord of the square on the board
        y: y-coord of the square on the board
        pawnId: player ID of the pawn that occupies this square. if none, pawnId=0
        neighbors: a list of squares neighboring this square"""
        self.x = x
        self.y = y
        self.pawnId = pawnId
        self.neighbors = neighbors

    def __str__(self):
        """Return a string representation of the square"""
        return "Square " + str((self.x,self.y))
    
class Wall:
    __slots__ = ('r1', 'c1', 'r2', 'c2', 'start', 'end', 'playerId')
    
    def __init__(self, r1, c1, r2, c2, playerId):
        
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2
        self.start = (r1, c1)
        self.end = (r2, c2)
        self.playerId = playerId
    def __str__(self):
        return "Wall from " + str((self.r1,self.c1)) + "to " + str((self.r2,self.c2))
        
    
    
    