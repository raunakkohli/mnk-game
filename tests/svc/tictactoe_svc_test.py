from datetime import datetime
from mnk.exceptions.mnk_exceptions import IllegalPlayerTurnException, InvalidGameStateException, InvalidMoveException

import pytest

from mnk.svc.tictactoe_service import TicTacToe
from mnk.models.tictactoe_models import CreateGameRequest, GameMode, GameStatus, TicTacToeData
from mnk.models.tictactoe_constants import Constants



class TestTicTacToeSvc:
    """
    Test cases for tic tac toe svc
    """

    def test_createNewGame(self):
        request = {
                    "mode": "SINGLE_PLAYER",
                    "player_1": "o",
                }
        game_request = CreateGameRequest(**request)
        game = TicTacToe.createGame(game_request)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "o"
        assert game.player_2 == Constants.DEFAULT_STARTING_PAWN
        assert game.player_turn == "o"
        assert len(game.moves) == 1
        assert game.created is not None


    def test_makeMove(self):
        
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="x")

        TicTacToe.makeMove("x", 0, 1, game)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "x"
        assert game.player_2 == "o"
        assert game.player_turn == "o"
        assert len(game.moves) == 1
        assert game.moves[0].pawn == "x"
        assert game.moves[0].row == 0
        assert game.moves[0].column == 1
        assert game.board[0][1] == "x"
        assert game.created is not None


    def test_makeMove_Invalid_game_state(self):
        
        game = TicTacToeData(id="123", status=GameStatus.PLAYER_1_WINS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="x")
        
        with pytest.raises(InvalidGameStateException) as e:
            TicTacToe.makeMove("x", 0, 1, game)

        assert str(e.value) == "Cannot make a move, since game is over."
    


    def test_makeMove_Invalid_move(self):
        
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="x")

        game.board[0][1] = "o"
        
        with pytest.raises(InvalidMoveException) as e:
            TicTacToe.makeMove("x", 0, 1, game)

        assert str(e.value) == "This move cannot be made. Select a valid and vacant spot."

    
    def test_makeMove_Invalid_move_out_of_bound(self):
        
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="x")
        
        with pytest.raises(InvalidMoveException) as e:
            TicTacToe.makeMove("x", -2, 1, game)

        assert str(e.value) == "This move cannot be made. Select a valid and vacant spot."
    

    def test_makeMove_Invalid_move_out_of_turn(self):
        
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="o")
        
        with pytest.raises(IllegalPlayerTurnException) as e:
            TicTacToe.makeMove("x", 2, 1, game)

        assert str(e.value) == "Move cannot be played out of turn."
        


    def test_autoMove(self):
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "",
        mode=GameMode.SINGLE_PLAYER, player_1="x", player_2="o",
        player_turn="x")
        
        TicTacToe.makeAutoMove(game)

        assert len(game.moves) == 1
        assert game.moves[0].pawn == "o"
        assert game.moves[0].row == 0
        assert game.moves[0].column == 0
        assert game.board[0][0] == "o"
        assert game.player_turn == "x"