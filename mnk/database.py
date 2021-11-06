
from datetime import datetime
from typing import Optional
import databases
import ormar
import sqlalchemy

from .config import settings



database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()



class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database



class Games(ormar.Model):
    class Meta(BaseMeta):
        tablename = "games"

    id: str = ormar.String(primary_key=True, max_length=128)
    mode: str = ormar.String(max_length=128, nullable=False)
    player_1_pawn: str = ormar.String(max_length=128, nullable=False)
    player_2_pawn: str = ormar.String(max_length=128, nullable=False)
    player_turn: str = ormar.String(max_length=128, nullable=False)
    status: str = ormar.String(max_length=128, nullable=False)
    created: datetime = ormar.DateTime(timezone=True, nullable=False)



class Moves(ormar.Model):
    class Meta(BaseMeta):
        tablename = "moves"

    id: int = ormar.Integer(primary_key=True)
    game: Optional[Games] = ormar.ForeignKey(Games, skip_reverse=True)
    pawn: str = ormar.String(max_length=128, nullable=False)
    row: int = ormar.Integer(nullable=False)
    column: int = ormar.Integer(nullable=False)
    created: datetime = ormar.DateTime(timezone=True, nullable=False)



engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)