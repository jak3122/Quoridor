"""
Quoridor II: Student Computer Engine

A sample class you may use to hold your state data
Author: Adam Oest (amo9149@rit.edu)

Author: Joe Ksiazek (jak3122@rit.edu)
"""

class EngineData(object):
    """A sample class for your engine data"""
    
    # Add other slots as needed
    __slots__ = ('logger', 'config', 'model', 'board')
    
    def __init__(self, logger, config, model, board):
        """
            Constructs and returns an instance of EngineData
            
            You decide what parameters and slots to use.  This is just a 
            minimal example.
            
            config: dict of parameters from config file
            model: 
            board: myBoard object
        """
        
        self.logger = logger
        self.config = config
        self.model = model
        self.board = board
        
        # initialize any other slots you require here
        
    def __str__(self):
        """
        __str__: EngineData -> string
        Returns a string representation of the EngineData object.
            self - the EngineData object
        """
        result = "EngineData= " \
                    + "logger: " + str(self.logger) \
                    + ", config: " + str(self.config) \
                    + ", model: " + str(self.model)
                
        # add any more string concatenation for your other slots here
                
        return result