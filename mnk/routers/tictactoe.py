import logging
import traceback

from fastapi import APIRouter, HTTPException
from mnk.models.tictactoe_constants import Constants
from ormar import NoMatch

from mnk.database import Games, Moves
from mnk.exceptions.mnk_exceptions import *
from mnk.models.tictactoe_models import *
from mnk.svc.tictactoe_service import TicTacToe
from mnk.repository.game_repository import GameRepo
from mnk.config import settings
from mnk.helpers.tictactoe_helper import getDateFromStr, getDateToStr


cache_enabled = settings.use_cache
router = APIRouter(prefix="/tictactoe")



# route to create a new game
@router.post("/", tags=["tictactoe"])
async def createNewGame(create_data: CreateGameRequest):
    """
    API to create a new game.
    """

    try:
        new_game: TicTacToeData = None
        # Initialise game data based on config
        new_game = TicTacToe.createGame(create_data)
        
        # persist the game
        try:
            # add game to db
            await Games.objects.create(id=new_game.id, mode=new_game.mode.value, 
            player_1_pawn=new_game.player_1, player_2_pawn=new_game.player_2, 
            player_turn=new_game.player_turn ,status=new_game.status.value,
            created=getDateFromStr(new_game.created))

            # If moves len is 1, then add that move to db (automove case)
            if len(new_game.moves) == 1:
                # reference to game for foreign key constraint
                game_fk = Games(id=new_game.id, mode=new_game.mode.value, player_1_pawn=new_game.player_1,
                player_2_pawn=new_game.player_2, player_turn=new_game.player_turn,
                status=new_game.status.value, created=getDateFromStr(new_game.created))
                move: Move = new_game.moves[0]
                # write to db
                await Moves.objects.create(game=game_fk, pawn=move.pawn, row=move.row, column=move.column, created=getDateFromStr(move.created))
            
            # add game to cache if caching enabled in config
            if cache_enabled:
                GameRepo.addGame(new_game)

        except:
            logging.error(traceback.format_exc())
            raise PersistenceException()
        
    except InvalidGameConfigException as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PersistenceException as e:
        raise HTTPException(status_code=502, detail=str(e))

    except:
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error occured.")

    
    response = {
        "game_id" : new_game.id,
        "game_board" : new_game.board,
        "game_status" : new_game.status,
        "player_1": new_game.player_1,
        "player_2": new_game.player_2,
        "player_turn" : new_game.player_turn
    }
    
    return response




# route to make a new move
@router.post("/move", tags=["tictactoe"])
async def makeNewMove(move_data: MakeMoveRequest):
    """
    API to make a move in a valid game.
    """

    # Get the game for which move is requested to be made
    try:
        game: TicTacToeData = None
        # if caching is enabled and game is in cache then read from there
        if cache_enabled:
            game = GameRepo.getGameById(move_data.game_id)

        if not game:
            try:
                # read game from db
                db_game:Games = await Games.objects.get(id=move_data.game_id)
                
                game = TicTacToeData(db_game.id, GameStatus[db_game.status],
                getDateToStr(db_game.created), mode=GameMode[db_game.mode], 
                player_1=db_game.player_1_pawn, player_2=db_game.player_2_pawn,
                player_turn=db_game.player_turn)

                #read corresponding moves from db (to get vacant spots and for winning logic)
                moves: List[Moves] = await Moves.objects.filter(game__id=db_game.id).all()
                game.moves = [Move(move.pawn, move.row, move.column, getDateToStr(move.created)) for move in moves]
                # update the vacant spots count
                game.number_of_vacant_cells -= len(game.moves)
                # update board with moves made so far
                for move in game.moves:
                    game.board[move.row][move.column] = move.pawn

                # add game to cache if caching enabled in config
                if cache_enabled:
                    GameRepo.addGame(game)

            except NoMatch as e:
                logging.error(traceback.format_exc())
                raise GameNotFoundException()

            except:
                logging.error(traceback.format_exc())
                raise PersistenceException()


        # make move based on mode and logic
        if game.mode == GameMode.SINGLE_PLAYER:
            TicTacToe.makeMove(move_data.pawn, move_data.row, move_data.column, game)
            TicTacToe.makeAutoMove(game)
        else:
            TicTacToe.makeMove(move_data.pawn, move_data.row, move_data.column, game)
        

        # persist the move made in db
        try:
            # reference to game for foreign key constraint
            game_fk = Games(id=game.id, mode=game.mode.value, player_1_pawn=game.player_1,
            player_2_pawn=game.player_2, player_turn=game.player_turn,
            status=game.status.value, created=getDateFromStr(game.created))
            
            last_move = len(game.moves)
            move: Move = game.moves[last_move-1]
            # write to db
            await Moves.objects.create(game=game_fk, pawn=move.pawn, row=move.row, column=move.column, created=getDateFromStr(move.created))
            
            # if automove was made then persist second last move as well
            if game.mode == GameMode.SINGLE_PLAYER:
                player_move: Move = game.moves[last_move-2]
                # write to db
                await Moves.objects.create(game=game_fk, pawn=player_move.pawn, row=player_move.row, column=player_move.column, created=getDateFromStr(player_move.created))
            
            # update game status and next player turn
            await Games.objects.filter(id__exact=game.id).update(player_turn=game.player_turn, status=game.status.value)

            # update game to cache if caching enabled in config
            if cache_enabled:
                GameRepo.addGame(game)

        except:
            logging.error(traceback.format_exc())
            raise PersistenceException()
        
    except GameNotFoundException as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PersistenceException as e:
        raise HTTPException(status_code=502, detail=str(e))

    except (InvalidMoveException, IllegalPlayerTurnException, InvalidGameStateException) as e:
        raise HTTPException(status_code=400, detail=str(e))

    
    response = {
        "game_id" : game.id,
        "game_board" : game.board,
        "game_status" : game.status,
        "player_1": game.player_1,
        "player_2": game.player_2,
        "player_turn" : game.player_turn,
        "moves" : game.moves
    }

    return response
