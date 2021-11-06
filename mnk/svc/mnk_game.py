from abc import ABC, abstractmethod


class AbstractMNKGame(ABC):

    """
    Parent Game Type.

    Game in which two players alternate placing stones of their own color on 
    an m-by-n board with the goal of getting k of their own color in a line. 
    It can have different variations and styles of play.
    """

    @abstractmethod
    def createGame(game_config):
        """
        Create a new game based on the game config
        """
        pass


    @abstractmethod
    def makeMove(game_id:int, player:int, location:tuple):
        """
        To make a player's move on the game board 
        """
        pass


