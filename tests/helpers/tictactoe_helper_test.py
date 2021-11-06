from datetime import datetime

import pytest

from mnk.helpers.tictactoe_helper import *



class TestTicTacToeHelper:
    """
    Test cases for tic tac toe helper methods
    """

    def test_getDateToStr(self):
        dt = datetime(2021,5,20)
        assert getDateToStr(dt) == "20/05/2021, 00:00:00:000000"


    def test_getDateFromStr(self):
        dt_str = "20/05/2021, 00:00:00:000000"
        assert getDateFromStr(dt_str) == datetime(2021,5,20)


    def test_getOnePlayerGame(self):
        request = {
                    "mode": "SINGLE_PLAYER",
                    "player_1": "x",
                }
        game_request = CreateGameRequest(**request)
        game = getOnePlayerGame(game_request)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "x"
        assert game.player_2 == Constants.DEFAULT_SECONDARY_PAWN
        assert game.player_turn == "x"
        assert game.created is not None


    def test_getOnePlayerGame_with_start_override(self):
        request = {
                    "mode": "SINGLE_PLAYER",
                    "player_1": "x",
                    "starting_pawn": "o"
                }
        game_request = CreateGameRequest(**request)
        game = getOnePlayerGame(game_request)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "x"
        assert game.player_2 == "o"
        assert game.player_turn == "o"
        assert game.created is not None

    
    def test_getTwoPlayerGame(self):
        request = {
                    "mode": "TWO_PLAYER",
                    "player_1": "o",
                    "player_2": "x"
                }
        game_request = CreateGameRequest(**request)
        game = getTwoPlayerGame(game_request)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "o"
        assert game.player_2 == "x"
        assert game.player_turn == "x"
        assert game.created is not None
    

    def test_getTwoPlayerGame_missing_p2(self):
        request = {
                    "mode": "TWO_PLAYER",
                    "player_1": "o"
                }
        game_request = CreateGameRequest(**request)
        game = getTwoPlayerGame(game_request)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "o"
        assert game.player_2 == "x"
        assert game.player_turn == "x"
        assert game.created is not None
    

    def test_getTwoPlayerGame_with_start_override(self):
        request = {
                    "mode": "TWO_PLAYER",
                    "player_1": "x",
                    "starting_pawn": "(o_o)"
                }
        game_request = CreateGameRequest(**request)
        game = getTwoPlayerGame(game_request)
        
        assert game.id is not None
        assert game.status == GameStatus.IN_PROGRESS
        assert game.player_1 == "x"
        assert game.player_2 == "(o_o)"
        assert game.player_turn == "(o_o)"
        assert game.created is not None
    

    def test_getTwoPlayerGame_InvalidGame_override(self):
        request = {
                    "mode": "TWO_PLAYER",
                    "player_1": "x",
                    "player_2": "y",
                    "starting_pawn": "(o_o)"
                }
        game_request = CreateGameRequest(**request)

        with pytest.raises(InvalidGameConfigException) as e:
            game = getTwoPlayerGame(game_request)

        assert str(e.value) == "Starting pawn does not match any provided player pawns."
    

    def test_getTwoPlayerGame_InvalidGame_unique_pawn(self):
        request = {
                    "mode": "TWO_PLAYER",
                    "player_1": "x",
                    "player_2": "x"
                }
        game_request = CreateGameRequest(**request)

        with pytest.raises(InvalidGameConfigException) as e:
            game = getTwoPlayerGame(game_request)
        
        assert str(e.value) == "Player_1 and Player_2 pawn value must be different."


    def test_isValidSpot_positive(self):
        assert isValidSpot(0,1,getInitialsedBoard()) == True


    def test_isValidSpot_negative_out_of_bound_spot(self):
        assert isValidSpot(-1,10,getInitialsedBoard()) == False
    

    def test_isValidSpot_negative_occupied_spot(self):
        game_board = getInitialsedBoard()
        game_board[0][1] = "x"
        assert isValidSpot(0,1,game_board) == False


    def test_updateStatus_row_win(self):
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="x")
        
        game.board[0][0] = "x"
        game.board[0][1] = "x"
        game.board[0][2] = "x"
        updateStatus(0,2,game)

        assert game.status == GameStatus.PLAYER_1_WINS


    def test_updateStatus_col_win(self):
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="x", player_2="o",
        player_turn="o")
        
        game.board[0][0] = "o"
        game.board[1][0] = "o"
        game.board[2][0] = "o"
        updateStatus(2,0,game)

        assert game.status == GameStatus.PLAYER_2_WINS


    def test_updateStatus_main_diagonal_win(self):
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="o", player_2="x",
        player_turn="o")
        
        game.board[0][0] = "o"
        game.board[1][1] = "o"
        game.board[2][2] = "o"
        updateStatus(2,2,game)

        assert game.status == GameStatus.PLAYER_1_WINS
    

    def test_updateStatus_reverse_diagonal_win(self):
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="o", player_2="x",
        player_turn="x")
        
        game.board[0][2] = "x"
        game.board[1][1] = "x"
        game.board[2][0] = "x"
        updateStatus(2,0,game)

        assert game.status == GameStatus.PLAYER_2_WINS


    def test_updateStatus_game_tied(self):
        game = TicTacToeData(id="123", status=GameStatus.IN_PROGRESS, created= "", 
        mode=GameMode.TWO_PLAYER, player_1="o", player_2="x",
        player_turn="x")
        
        game.board[0][0] = "o"
        game.board[0][1] = "o"
        game.board[0][2] = "x"
        game.board[1][0] = "x"
        game.board[1][1] = "x"
        game.board[1][2] = "o"
        game.board[2][0] = "o"
        game.board[2][1] = "x"
        game.board[2][2] = "x"
        game.number_of_vacant_cells = 0
        updateStatus(2,2,game)

        assert game.status == GameStatus.TIED