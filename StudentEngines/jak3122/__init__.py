"""
Student Quoridor Engine Module        
Author: Adam Oest (amo9149@rit.edu)

Author: Wheeler Law (wpl3499@rit.edu)
Author: Joe Ksiazek (jak3122@rit.edu)
    
This is where you will be able to define all the
methods that control the flow of execution of the game
"""
from Model.interface import PlayerMove
from Model.interface import BOARD_DIM
from Engine.security import GameException
from Engine.logger import Logger
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
    Logger.write(Logger,"VALIDATION: Validating.........")
    player_id = playerMove.playerId
    is_pawn_move = playerMove.move
    
    if is_pawn_move:
        
        start_r, start_c = playerMove.start
        end_r, end_c = playerMove.end
        start_square = engineData.board.squares[(start_r, start_c)]
        
        
        # 2a
        # check if player and engine pawn start locations match
        if not start_square.pawnId == player_id:
            Logger.error(Logger,"VALIDATION: Engine/player start square mismatch.")
            return False
        
        # 2b
        # check if end location is on the board
        
        within_bounds = (0 <= end_r <= BOARD_DIM-1) and (0 <= end_c <= BOARD_DIM-1)
        if not within_bounds:
            Logger.error(Logger,"VALIDATION ERROR: End square out of bounds.")
            return False
        
        # 2c
        # check if end location is an accessible neighbor of start location
        start_square.neighbors = get_neighbors(engineData, start_r, start_c)
        if not list((end_r, end_c)) in start_square.neighbors:
            # get_neighbors checks if the neighbors are accessible,
            # so we don't need to do that here
            Logger.error(Logger,"VALIDATION ERROR: End square not accessible.")
            return False
        
    else: # wall move
        
        m = engineData.model.getPlayerData(player_id)['model'] 
        walls_remaining = m.playerWallsRemaining
        player_positions = m.playerPositions
        walls = m.walls
        player_goals = m.playerGoals
        
        # 1a
        # check that there's enough walls left
        if walls_remaining[player_id-1] <= 0:
            Logger.error(Logger,"VALIDATION ERROR: No walls remaining for player.")
            return False
        
        # 1b
        # check that length of wall is 2 units
        # 1c
        # make sure wall coords are legal and in bounds
        # 1d
        # make sure the top/left coord pair is in r1/c1 (start) slot
        # 1e
        # make sure wall is vertical or horizontal, not diagonal
        wall_height = playerMove.r2 - playerMove.r1
        wall_width = playerMove.c2 - playerMove.c1
        vertical_wall = wall_height == 2 and wall_width == 0
        horiz_wall = wall_height == 0 and wall_width == 2        
        
        if vertical_wall:
            legal_r1 = 0 <= playerMove.r1 <= 7
            legal_c1 = 1 <= playerMove.c1 <= 8
            legal_r2 = 2 <= playerMove.r2 <= 9
            legal_c2 = 1 <= playerMove.c2 <= 8
        elif horiz_wall:
            legal_r1 = 1 <= playerMove.r1 <= 8
            legal_c1 = 0 <= playerMove.c1 <= 7
            legal_r2 = 1 <= playerMove.r2 <= 8
            legal_c2 = 2 <= playerMove.c2 <= 9
        else:
            Logger.error(Logger,"VALIDATION ERROR: Walls are improper size.")
            return False
        
        if not legal_r1 and legal_c1 and legal_r2 and legal_c2:
            Logger.error(Logger,"VALIDATION ERROR: Invalid wall coordinates.")
            return False
            
        
        
        # 1f
        # make sure wall doesn't cross over any other walls
        
        #something to note: when walls cross over each other,
        # it means that their center points are touching. 
        center_point=(int((playerMove.r1+playerMove.r2)/2),int((playerMove.c1+playerMove.c2)/2))
        for i in range(0,len(walls)):
            temp_center_point=(int((walls[i][0]+walls[i][2])/2),int((walls[i][1]+walls[i][3])/2))
            if center_point==temp_center_point:
                Logger.error(Logger,"VALIDATION ERROR: Invalid wall placement, overlaps valid wall.")
                return False
            
        #overlapping walls are a little trickier. Walls overlapping completely
        #have their center points touching, but walls that are only overlapping
        #one section do not. So things get a little trickier. Basically the 
        #center point of the wall to be placed has to be touching an end point
        # of another wall AND they have the be in the same direction. 
        
        stop=0 #needed this for a break point. does nothing. 
        
        for i in range(0,len(walls)):
            
            #determine direction of walls already places
            height=walls[i][2]-walls[i][0]
            width=walls[i][3]-walls[i][1]
            if height==0: #horizontal: True, vertical: False
                direction=True
            else:
                direction=False
                
            end_point_N=(walls[i][0],walls[i][1])
            if end_point_N==center_point and direction==horiz_wall: #notice a pattern?
                Logger.error(Logger,"VALIDATION ERROR: Invalid wall placement, overlaps valid wall.")
                return False
                return False
            
            end_point_S=(walls[i][2],walls[i][3])
            if end_point_S==center_point and direction==horiz_wall:
                Logger.error(Logger,"VALIDATION ERROR: invalid wall placement, overlaps valid wall.")
                return False
                return False
        
        
        # 1g
        # check that new wall placement doesn't interfere with any pawn
        # getting to their goal
        
        engineData_test=last_move(engineData,playerMove)
        
        available=0 #number of goal squares accessible to the pawn. At the start
                    #of the game, it is 9, but then goes down as you block them off.
                    
        for i in range(0,9):
            path=get_shortest_path(\
                                   engineData_test,\
                                   player_positions[0][0],\
                                   player_positions[0][1],\
                                   player_goals[0][i][0],\
                                   player_goals[0][i][1]\
                                   )
            #I dont know if playerGoals attribute is the same for every player, so I have it 
            #set up for player one. Same goes for positions. 

            if path!=[]:
                available=available+1
        
        if available==0:
            Logger.error(Logger,"VALIDATION ERROR: Invalid wall placement, blocks player from reaching home.")
            return False
        
    
    return True

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
    model=engineData.model
    
    # Step 2
    # Get the player module from the model using model.getPlayerModule.
    playermodule=model.getPlayerModule(playerNum)
    
    # Step 3
    # Call the chosen player module's init function with the appropriate data.
    #
    # Tips:
    # logger was already given to you in your own init method
    # numWalls depends on the number of players and is accessible through the
    #     NUM_WALLS key in the config dictionary
    # playerHomes may only include home locations for active players in the game
    #     and it must be a tuple, not a list.
    logger=engineData.logger
    numWalls=engineData.config['NUM_WALLS'][len(model.playerHomes)]
    playermodule=playermodule.init(logger,playerNum,numWalls, model.playerHomes)
    # Step 4
    # Save the player data using StudentEngineModel's setPlayerData method.
    # The StudentEngineModel object should have been saved when your init
    # function was called.
    model.setPlayerData(playerNum,playermodule)
    
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
        
                      
        Parameter:
            engineData: the data originally built by this module in init()
                        (used to establish the context of the move)
            playerNum: the number of the player (in [0 .. n-1] for n players)

        returns: the engine data, modified by the actions described above
    """
    
    # Step 1
    # Get playerMove object from the current player using player module's move
    # function.
    # (At this point you do not need to record any player's playerData.)
    playerNum=engineData.move
    numPlayers=len(engineData.model.playerHomes)
    
    model=engineData.model
    playermodule=model.getPlayerModule(playerNum)
    playerdata=model.getPlayerData(playerNum)
    
    move=playermodule.move(playerdata)
    move=move.getCopy()
    
    # Step 2
    # Validate the move.
    valid=validate_move(engineData,move)

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
    
    if valid==False:
        exit_due_to_error("INVALID MOVE")
        engineData.logger.error("INVALID MOVE")
    else:
        
            
        engineData=last_move(engineData,move)
        model.makeMove(move)
        
        for player in range(1,numPlayers+1): #update all other players' boards. 
            playerdata=model.getPlayerData(player) #get player data
            playerdata=playermodule.last_move(playerdata,move) #update the board
            model.setPlayerData(playerNum,playerdata)
            
        engineData.move=engineData.move+1 #keep count of what player it is right now
        if engineData.move>numPlayers:
            engineData.move=1
        

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
    