from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pydantic.main import BaseModel

from .game_data import MNKGameData



## Enums

class GameStatus(Enum):
    """
    Tic Tac Toe Game can have different statuses, depending on the progress
    """
    CREATED = 'CREATED'
    IN_PROGRESS = 'IN_PROGRESS'
    TIED = 'TIED'
    PLAYER_1_WINS = 'PLAYER_1_WINS'
    PLAYER_2_WINS = 'PLAYER_2_WINS'


class GameMode(Enum):
    """
    Tic Tac Toe Game can have different modes in which it can be played 
    """
    SINGLE_PLAYER = 'SINGLE_PLAYER'
    TWO_PLAYER = 'TWO_PLAYER'




## Data Models

@dataclass
class Move:
    pawn: str
    row: int
    column: int
    created: str # dateTime in str for showing in json response


# helper method for dataclass field init
def getInitialsedBoard():
    return [['-' for _ in range(3)] for _ in range(3)] # make a 3x3 matrix | '-' => vacant spot

@dataclass
class TicTacToeData(MNKGameData):
    mode: GameMode
    player_1: str
    player_2: str
    player_turn: str
    board: List[List[int]] = field(default_factory=getInitialsedBoard)
    moves: List[Move] = field(default_factory=list)
    number_of_vacant_cells: int = 9 # initially the 3x3 board would be empty, so all 9 are available





## Pydantic Request Models

class CreateGameRequest(BaseModel):
    mode: GameMode
    player_1: str # player 1 pawn
    player_2: Optional[str] # player 2 pawn can be computer in case of SINGLE_PLAYER mode
    starting_pawn: Optional[str] = None # Override the default 'x' starting pawn


class MakeMoveRequest(BaseModel):
    game_id: str # game reference id generated during game creation
    pawn: str
    row: int 
    column: int  
    
