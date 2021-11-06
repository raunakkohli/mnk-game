from datetime import datetime, timedelta
import logging
from cachetools import TTLCache

from mnk.models.tictactoe_models import TicTacToeData


class GameRepo:
    """
    This class will be the means to access all games. 
    """

    # A LRU TTL cache (eviction based on least recently used with time expiration)
    game_cache = TTLCache(maxsize=100, ttl=timedelta(seconds=30), timer=datetime.now)


    def addGame(game_data: TicTacToeData) -> None:
        GameRepo.game_cache[game_data.id] = game_data    
        logging.info("cache updated")    


    def getGameById(game_id: str) -> TicTacToeData:
        # get from cache if possible
        logging.info("cache read")
        return GameRepo.game_cache.get(game_id, None)


    def _clearCache() -> None:
        """
        To flush the cache if needed
        """
        GameRepo.game_cache.clear()
