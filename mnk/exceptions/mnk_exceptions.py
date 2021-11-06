"""
Exceptions that can arise in a m-n-k game
"""

class InvalidGameConfigException(Exception):
    """
    Thrown when attempted to make a move when the game is already over
    """
    def __init__(self, message):
        super().__init__(message)


class InvalidGameStateException(Exception):
    """
    Thrown when attempted to make a move when the game is already over
    """
    def __init__(self):
        message = 'Cannot make a move, since game is over.'
        super().__init__(message)


class InvalidMoveException(Exception):
    """
    Thrown when the move is made in a wrong game cell(position).
    """
    def __init__(self):
        message = 'This move cannot be made. Select a valid and vacant spot.'
        super().__init__(message)


class IllegalPlayerTurnException(Exception):
    """
    Thrown when player attempted to make a move outside of their turn.
    """
    def __init__(self):
        message = 'Move cannot be played out of turn.'
        super().__init__(message)


class PersistenceException(Exception):
    """
    Thrown when issue occured while persisting data.
    """
    def __init__(self):
        message = 'There was an issue with the database.'
        super().__init__(message)


class GameNotFoundException(Exception):
    """
    Thrown when issue occured while persisting data.
    """
    def __init__(self):
        message = 'The game against which operation was attempted does not exist.'
        super().__init__(message)