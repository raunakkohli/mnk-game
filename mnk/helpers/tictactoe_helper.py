from datetime import datetime
from typing import List
from uuid import uuid4

from mnk.models.tictactoe_constants import Constants
from mnk.models.tictactoe_models import *
from mnk.exceptions.mnk_exceptions import *



## Helper methods for tictactoe router and service


## Router helpers
def getDateToStr(date_val:datetime):
    return date_val.strftime(Constants.DATE_FORMAT)


def getDateFromStr(str_date: str):
    return datetime.strptime(str_date, Constants.DATE_FORMAT)



## Service helpers
def getOnePlayerGame(game_data: CreateGameRequest) -> TicTacToeData:
    """
    In a SINGLE_PLAYER game player_2 would be the computer. 
    We need to be setting the pawn for the same accordingly,
    and if the starting player is computer then make a move and update the game
    """
    curr_player_turn = None
    # check if override is provided
    if game_data.starting_pawn:
        # scenario 1) player 1 is not the starting pawn
        if game_data.player_1 != game_data.starting_pawn:
            game_data.player_2 = game_data.starting_pawn
            curr_player_turn = game_data.player_2
        
        # scenario 2) player 1 is the starting pawn
        else:
            game_data.player_2 = Constants.DEFAULT_STARTING_PAWN if (game_data.starting_pawn != Constants.DEFAULT_STARTING_PAWN) else Constants.DEFAULT_SECONDARY_PAWN
            curr_player_turn = game_data.player_1
    
    else:
        # initialise player 2 and current_player data based on default starting pawn
        game_data.player_2 = Constants.DEFAULT_STARTING_PAWN if (game_data.player_1 != Constants.DEFAULT_STARTING_PAWN) else Constants.DEFAULT_SECONDARY_PAWN
        curr_player_turn = game_data.player_1 if (game_data.player_1 == Constants.DEFAULT_STARTING_PAWN) else game_data.player_2

    # Generate new id and set status to created, with other initialised data
    return TicTacToeData(id=str(uuid4()), status=GameStatus.IN_PROGRESS, 
        created=datetime.now().astimezone().strftime(Constants.DATE_FORMAT), mode=game_data.mode, 
        player_turn=curr_player_turn, player_1=game_data.player_1, player_2= game_data.player_2)
    


def getTwoPlayerGame(game_data: CreateGameRequest) -> TicTacToeData:
    curr_player_turn = None

    # 1) check if player 2 provided, else initialse it if possible
    if not game_data.player_2:
        # Override check for initialising player 2
        if game_data.starting_pawn:
            if game_data.player_1 == game_data.starting_pawn:
                game_data.player_2 = Constants.DEFAULT_STARTING_PAWN if(game_data.starting_pawn != Constants.DEFAULT_STARTING_PAWN) else Constants.DEFAULT_SECONDARY_PAWN
            else:
                game_data.player_2 = game_data.starting_pawn
        else:
            game_data.player_2 = Constants.DEFAULT_STARTING_PAWN if(game_data.player_1 != Constants.DEFAULT_STARTING_PAWN) else Constants.DEFAULT_SECONDARY_PAWN

    # 2) check if player 1 and 2 pawns are unique
    if game_data.player_1 != game_data.player_2:
        # get current player turn value based on starting pawn config
        # 3) check if starting pawn override has been provided
        if game_data.starting_pawn and (game_data.player_1 == game_data.starting_pawn 
        or game_data.player_2 == game_data.starting_pawn):
            curr_player_turn = game_data.player_1 if (game_data.player_1 == game_data.starting_pawn) else game_data.player_2
        
        # 4) check if any player pawns match default starting pawn
        elif (not game_data.starting_pawn) and (game_data.player_1 == Constants.DEFAULT_STARTING_PAWN 
        or game_data.player_2 == Constants.DEFAULT_STARTING_PAWN):
            curr_player_turn = game_data.player_1 if (game_data.player_1 == Constants.DEFAULT_STARTING_PAWN) else game_data.player_2

        else:
            raise InvalidGameConfigException("Starting pawn does not match any provided player pawns.")
    else:
        raise InvalidGameConfigException("Player_1 and Player_2 pawn value must be different.")

    # Generate new id and set status to created, with other initialised data
    return TicTacToeData(id=str(uuid4()), status=GameStatus.IN_PROGRESS, 
        created=datetime.now().astimezone().strftime(Constants.DATE_FORMAT), mode=game_data.mode, player_turn=curr_player_turn,
        player_1=game_data.player_1, player_2= game_data.player_2)



def isValidSpot(row:int, col:int, board: List[List[int]]) -> bool:
    """
    check if cell attempted to fill is available/empty 
    """
    if row<0 or row>2 or col<0 or col>2:
        return False
    return board[row][col] == '-'



def __isRowComplete(row_number, board: List[List[int]], pawn:str) -> bool:
    """
    checks if all the cells in the given row have same value
    Value checked with the current player number 
    """
    for spot in board[row_number]:
        if spot != pawn:
            return False
    return True 



def __isColumnComplete(col_number, board: List[List[int]], pawn:str) -> bool:
    """
    checks if all the cells in the given column have same value
    Value checked with the current player number 
    """
    for row in range(3):
        if board[row][col_number] != pawn:
            return False
    return True



def __isMainDiagonalComplete(board: List[List[int]], pawn:str) -> bool:
    """
    checks if all the cells in the main diagonal have same value
    Value checked with the current player number 
    """
    # start from top-left, move to bottom-right
    for index in range(3):
        if board[index][index] != pawn:
            return False
    return True



def __isReverseDiagonalComplete(board: List[List[int]], pawn:str) -> bool:
    """
    checks if all the cells in the reverse diagonal have same value
    Value checked with the current player number
    """
    row, col = 0, 2 # start from top-right
    for _ in range(3):
        if board[row][col] != pawn:
            return False
        # # start from top-right
        row += 1
        col -= 1
    return True

    

def updateStatus(row:int, col:int, game: TicTacToeData) -> None:
    """
    checks if any player has won, tied or game can proceed
    """
    
    # if criteria is met then player has won
    # check the row, column and diagonals for win possibility
    if __isRowComplete(row, game.board, game.player_turn):
        game.status = GameStatus.PLAYER_1_WINS if (game.player_turn == game.player_1) else GameStatus.PLAYER_2_WINS

    elif __isColumnComplete(col, game.board, game.player_turn):
        game.status = GameStatus.PLAYER_1_WINS if (game.player_turn == game.player_1) else GameStatus.PLAYER_2_WINS

    # if row and col have same value then element lies on main diagonal
    elif row == col and __isMainDiagonalComplete(game.board, game.player_turn):
        game.status = GameStatus.PLAYER_1_WINS if (game.player_turn == game.player_1) else GameStatus.PLAYER_2_WINS

    # if row and (3[board size] - 1 - col)are same then element lies on reverse diagonal 
    elif row == (2 - col) and __isReverseDiagonalComplete(game.board, game.player_turn):
        game.status = GameStatus.PLAYER_1_WINS if (game.player_turn == game.player_1) else GameStatus.PLAYER_2_WINS
        
    elif game.number_of_vacant_cells == 0:
        # if criteria is not met and no more cells available to make a move then TIE
        game.status = GameStatus.TIED
    # else the game status stays "IN_PROGRESS"
