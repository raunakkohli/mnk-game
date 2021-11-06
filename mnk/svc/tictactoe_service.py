from datetime import datetime

from .mnk_game import AbstractMNKGame
from mnk.models.tictactoe_constants import Constants
from mnk.models.tictactoe_models import *
from mnk.exceptions.mnk_exceptions import *
from mnk.helpers import tictactoe_helper



class TicTacToe(AbstractMNKGame):

    """
    Tic Tac Toe Game Doc
    _____________________

    It is the most popular version of a M-N-K Game.
    It's played on 3x3 board by 2 players with their respective pawn each, 
    generally 'x' and 'o'.
    To win a player must fill 3 number of continuous cells in any direction.
    (Possible directions: horizontal, vertical, diagonal) 
    """


    def createGame(game_config: CreateGameRequest):
        """
        Creates a new tic tac toe game based on the configuration provided
        """
        new_game = None
        if game_config.mode == GameMode.SINGLE_PLAYER:
            new_game = tictactoe_helper.getOnePlayerGame(game_config)
            # If computer move is first, then make an auto move and update the game
            if new_game.player_2 == new_game.player_turn:
                TicTacToe.makeAutoMove(new_game)
            return new_game

        else:
            new_game = tictactoe_helper.getTwoPlayerGame(game_config)
        
        return new_game



    def makeMove(pawn:str, row:int, col: int, game: TicTacToeData) -> None:
        """
        Updates cell on board where player has made a move if valid, else throws Exception
        """

        # Validate the move trying to be made
        if game.status == GameStatus.IN_PROGRESS:
            if pawn == game.player_turn:
                if (game.number_of_vacant_cells>0) and tictactoe_helper.isValidSpot(row, col, game.board):
                
                    # set move on board
                    game.board[row][col] = pawn
                    # decrease count of valid spots
                    game.number_of_vacant_cells -= 1
                    # record the move made
                    game.moves.append(Move(pawn, row, col, datetime.now().astimezone().strftime(Constants.DATE_FORMAT)))
                    
                    # update status of the game
                    tictactoe_helper.updateStatus(row, col, game)

                    # Update next player
                    game.player_turn = game.player_1 if(game.player_turn == game.player_2) else game.player_2
                
                else:
                    raise InvalidMoveException()

            else:
                raise IllegalPlayerTurnException()

        else:
            raise InvalidGameStateException()




    def makeAutoMove(game_data: TicTacToeData):
        # note: player 2 is computer
        if (game_data.number_of_vacant_cells > 0) and (game_data.status==GameStatus.IN_PROGRESS):

            start_row, start_col = 0,0
            end_row, end_col = 2,2
            board = game_data.board
            selected_location = None
            
            # check the first and last positions on board for vacancy
            # iterate this way until vacany spot found
            while not (start_row>=end_row and start_col>=end_col):
                
                if board[start_row][start_col] == '-':
                    selected_location = (start_row, start_col)
                    break
                
                elif board[end_row][end_col] == '-':
                    selected_location = (end_row, end_col)
                    break
                
                # moving starting pointer left->right, top->bottom
                start_row = (start_row+1) if start_col==2 else start_row
                start_col = (start_col+1) if start_col!=2 else 0

                # moving end pointer right->left, bottom->top
                end_row = (end_row-1) if end_col==0 else end_row
                end_col = (end_col-1) if end_col!=0 else 2

            # Update the game board and the next player
            game_data.board[selected_location[0]][selected_location[1]] = game_data.player_2
            # decrease count of valid spots
            game_data.number_of_vacant_cells -= 1
            # record the move made
            game_data.moves.append(Move(game_data.player_2, selected_location[0], selected_location[1], datetime.now().astimezone().strftime(Constants.DATE_FORMAT)))
            # update status of the game
            tictactoe_helper.updateStatus(selected_location[0], selected_location[1], game_data)
            # Update the next player
            game_data.player_turn = game_data.player_1
            