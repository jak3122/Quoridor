"""
Student Quoridor Engine Module        
Author: Adam Oest (amo9149@rit.edu)
    
This is where you will be able to define all the
methods that control the flow of execution of the game
"""
from Model.interface import PlayerMove
from Model.interface import BOARD_DIM
from Engine.security import GameException
from .engineData import EngineData
from .myBoard import *
from .myQueue import *
from .myStack import *


"""
Quoridor II: Student Engine
Author: Adam Oest (amo9149@rit.edu)

Implement the methods in the order you see them

Author: JOE KSIAZEK (jak3122@rit.edu)
"""

def init(logger, config, studentModel):
    """
        Part 1 - 4
    
        The system calls this function once at the beginning of the game.
        The student engine uses this function to initialize its data
        structures to the initial game state.

        Parameters
            logger: a reference to the logger object. The player model uses
                logger.write(msg) and logger.error(msg) to log diagnostic
                information.
                
            config: a Python 'dict' structure that has mapped all the
                parameter names to their values, as specified in the
                config.cfg file.
        
            studentModel: reference to a StudentEngineModel object. See
                the documentation for that class in the file
                Model/interface.py. This engine calls the methods in
                that object.
        returns:
            a data structure that stores all of the engine's needed data
    """
    NewBoard = Board()
    
    # initialize pawns on their home squares
    homes = studentModel.playerHomes
    id_counter = 1
    for home in homes:
        NewBoard.squares[home].pawnId = id_counter
        id_counter += 1
    engineData = EngineData(logger, config, studentModel, NewBoard)
    
    return engineData

def last_move(engineData, playerMove):
    """
        Parts 1 and 2 only; in parts 3 and 4, this engine will be controlling
        the players.
        
        The system calls this function after a player makes a valid move in
        the game. The student engine updates its data structure with the
        information about the move.

        Parameters
            engineData: this engine's data, originally built by this
                        module in init()
        
            playerMove: the instance of PlayerMove that describes the
                        move just made
        
        returns:
            this player module's updated (engineData) data structure
    """
    
    # Update your engineData board state here, incorporating the last move.
    the_board = engineData.board
    is_pawn_move = playerMove.move
    if is_pawn_move:
        source_coord = playerMove.start
        dest_coord = playerMove.end
        
        the_board.squares[source_coord].pawnId = 0                     # remove pawn from source square
        the_board.squares[dest_coord].pawnId = playerMove.playerId     # move the pawn to dest square
            
    else:                   # wall was placed
        the_board.addWall(playerMove.r1, playerMove.c1, playerMove.r2, playerMove.c2)

    return engineData

def get_neighbors(engineData, r, c):
    """
        Part 1
    
        This function is used only in part 1 mode. The system calls it after
        all PRE_MOVEs have been made. (See the config.cfg file.)

        Parameters
            engineData: the data originally built by this module in init()
            r: row coordinate of starting position for this player's piece
            c: column coordinate of starting position for this player's piece
        
        returns:
            a list of coordinate pairs (a list of lists, e.g. [[0,0], [0,2]],
            not a list of tuples) denoting all the reachable neighboring squares
            from the given coordinate. "Neighboring" means exactly one move
            away.
    """
    
    # Use your engineData object to get a list of neighbors
    neighbors = [
                 [r, c-1],
                 [r-1, c],
                 [r, c+1],
                 [r+1, c]
                 ]
    final_neighbors = []
    wall_list = engineData.board.walls
    for n in neighbors:
        row = n[0]
        col = n[1]
        
        wall_in_the_way = False
        for wall in wall_list:
            if n == neighbors[0]:   # left neighbor
                if ((wall.r1, wall.c1) == (r, c) and (wall.r2, wall.c2) == (r+2, c)) or ((wall.r1, wall.c1) == (r-1, c) and (wall.r2, wall.c2) == (r+1, c)):
                    wall_in_the_way = True
                    
            elif n == neighbors[1]: # top neighbor
                if ((wall.r1, wall.c1) == (r, c) and (wall.r2, wall.c2) == (r, c+2)) or ((wall.r1, wall.c1) == (r, c-1) and (wall.r2, wall.c2) == (r, c+1)):
                    wall_in_the_way = True
                    
            elif n == neighbors[2]:  # right neighbor
                if ((wall.r1, wall.c1) == (r, c+1) and (wall.r2, wall.c2) == (r+2, c+1)) or ((wall.r1, wall.c1) == (r-1, c+1) and (wall.r2, wall.c2) == (r+1, c+1)):
                    wall_in_the_way = True
                    
            elif n == neighbors[3]: # bottom neighbor
                if ((wall.r1, wall.c1) == (r+1, c) and (wall.r2, wall.c2) == (r+1, c+2)) or ((wall.r1, wall.c1) == (r+1, c-1) and (wall.r2, wall.c2) == (r+1, c+1)):
                    wall_in_the_way = True
                    
            else:
                print("Error in for-loop line ~137")
                input()
        
        if not(row < 0 or col < 0 or row > 8 or col > 8 or wall_in_the_way):
            final_neighbors.append(n)

    return final_neighbors

def get_shortest_path(engineData, r1, c1, r2, c2):
    """
        Part 1
    
        This function is only called in part 1 mode. The engine calls it when
        a shortest path is requested by the user via the graphical interface.

        Parameters
            engineData: the data originally built by this module in init()
            r1: row coordinate of starting position
            c1: column coordinate of starting position
            r2: row coordinate of destination position
            c2: column coordinate of destination position
        
        returns:
            a list of coordinates that form the shortest path from the starting
            position to the destination, inclusive. The format is an ordered
            list of coordinate pairs (a list of lists, e.g.,
            [[0,0], [0,1], [1,1]], not a list of tuples).
            If there is no path, an empty list, [], should be returned.
    """
    
    # Use your engineData object to find a shortest path using breadth-first
    # search (BFS).
    # You will probably find the get_neighbors function helpful.
    
    predecessors = {}
    queue = Queue()
    start_square = (r1,c1)
    end_square = (r2,c2)
    
    enqueue(start_square, queue)
    predecessors[start_square] = None
    while not emptyQueue(queue):
        current = front(queue)
        dequeue(queue)
        if current == end_square:
            break
        neigh_coords = get_neighbors(engineData, current[0], current[1])
        neighbors = []
        for n in neigh_coords:
            neighbors.append(tuple(n))
        for neighbor in neighbors:
            #NeighSquare = Square(neighbor[0], neighbor[1])
            if neighbor not in predecessors:
                predecessors[neighbor] = current
                enqueue(neighbor, queue)
    return constructPath(predecessors, start_square, end_square)

def constructPath(predecessors, source, destination):
    """
    Returns a path from source to destination.
    """
    stack = Stack()
    if destination in predecessors:
        tmp = destination
        while tmp != source:
            push(tmp, stack)
            tmp = predecessors[tmp]
        push(source, stack)
    
    path = []
    while not emptyStack(stack):
        path.append(top(stack))
        pop(stack)
        
    return path
        
def validate_move(engineData, playerMove):
    """
        Check to see if the given move is valid for the given game state.
        
        In part 2 this function is called by the system.
        In parts 3 and 4 the function is called internally by the player
        engine itself from next_move().

        Parameters
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerMove: the instance of PlayerMove that describes the
                        move just made
        Returns: a bool representing whether or not the given move is valid
    """
    print("In validate_move")
    player_id = playerMove.playerId
    is_pawn_move = playerMove.move
    is_valid_move = True # the main flag for this function which gets returned
    
    if is_pawn_move:
        
        
        # check if player and engine pawn start locations match
        r, c = playerMove.r1, playerMove.c1
        print("Pawn move")
        print("Player id:", player_id)
        print("r,c:", (r,c))
        print("squares[(r,c)]:", engineData.board.squares[(r,c)])
        print("squares[(r,c)].pawnId:", engineData.board.squares[(r,c)].pawnId)
        
        if not engineData.board.squares[(r,c)].pawnId == player_id:
            
            print("Engine/player start square mismatch") # replace with logger call
            is_valid_move = False
        
    else: # wall move
        print("Wall move")
        
        m = engineData.model.getPlayerData(player_id)['model'] # 
    

    input()
    return is_valid_move

def initialize_player(engineData, playerNum):
    """
        Part 3 and 4
        The system calls this function when it wants the student engine
        to initialize a specific player module via its init() function.
        
        Reference file for init(): StudentPlayers/RenameYourPlayer/__init__.py
        
        Parameters
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerNum: the number of the player (in [0 .. n-1] for n players)

        returns: the engine data, modified
    """
    
    # Step 1
    # Fetch the reference to the model from your engineData.
    model = None
    
    # Step 2
    # Get the player module from the model using model.getPlayerModule.
    
    # Step 3
    # Call the chosen player module's init function with the appropriate data.
    #
    # Tips:
    # logger was already given to you in your own init method
    # numWalls depends on the number of players and is accessible through the
    #     NUM_WALLS key in the config dictionary
    # playerHomes may only include home locations for active players in the game
    #     and it must be a tuple, not a list.
    
    # Step 4
    # Save the player data using StudentEngineModel's setPlayerData method.
    # The StudentEngineModel object should have been saved when your init
    # function was called.
    
    return engineData

def next_move(engineData):
    """
        Part 3 and 4
        
        Ask the module of the player whose turn it is for its next move
        (player's move function.)
        Check the move for validity. If invalid, exit_due_to_error is called.
        If valid, all player modules are notified of the move via last_move.

        Process the next move, sending it to the engine
                      and notifying other players
        
                      
        Parameters
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerNum: the number of the player (in [0 .. n-1] for n players)

        returns: the engine data, modified by the actions described above
    """
    
    # Step 1
    # Get playerMove object from the current player using player module's move
    # function.
    # (At this point you do not need to record any player's playerData.)
    
    # Step 2
    # Validate the move.

    # Step 3
    # If it is invalid:
    #     Call exit_due_to_error (contained in this file).
    # else:
    #     Update your engineData board state.
    #     Call the makeMove function in your model object.
    #         The StudentEngineModel object should have been saved when your
    #         init function was called.
    #
    #     Notify all players of this move by doing the following
    #         for each player:
    #             Call player.last_move(playerData, playerMove).
    #             Save the player's returned playerData using
    #                                           model.setPlayerData
    #
    #     [ !!! Obtain playerData using model.getPlayerData ??? ]
    
    # Safety tip: rather than passing the playerMove object, pass a copy of it
    # by calling playerMove.getCopy() to ensure that there is no harm done if
    # the original object gets modified.

    # Development tip: Disable AUTO_PLAY in config.cfg while developing this.

    return engineData

def exit_due_to_error(message):
    """
        Part 3 and 4: Exit the program 
                      after a player makes an illegal move
        This is an INTERNAL function called from next_move above, when
        that function has determined that the move chosen by the player
        violates the rules of the game.

        Parameters
            message: the error message to be displayed in the user interface
    """
    
    # NOTE: You do not need to edit the code in this function at all!
    
    raise GameException(message)

def generate_board(engineData):
    """    
        Part 4: Generate a symmetric board configuration
        
        engineData: your engine state
        
        moveExecFunction: call with moves
        
        returns: your engine state
    """
    # Hint: disable AUTO_PLAY while developing this
        
    
    # numWalls equals the value of the STUDENT_ENGINE_WALLS config parameter
    # this controls how many PlayerMoves you generate in this function
    # note that this number should always be even due to the asymmetry of the
    # game board
    numWalls = None
    
    # Generate PlayerMoves to be made
    
    # For each move:
    #     call model.makeMove(playerMove)
    #     notify players of this move
    
    return engineData
    