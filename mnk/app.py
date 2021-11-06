import logging

from fastapi import FastAPI
from mnk.routers import tictactoe
from mnk.database import database
from .config import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

cache_enabled = settings.use_cache

tags_metadata = [
    {
        "name": "tictactoe",
        "description": "Operations performed on tictactoe, like creating a game and making a move.",
    },
]

app = FastAPI(openapi_tags=tags_metadata, title="TicTacToe")

app.include_router(tictactoe.router)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    
    logging.info("APP STARTED!")
    logging.info(f"Config | In memory cache enabled: {cache_enabled}")



@app.on_event("shutdown")
async def shutdown():
    logging.INFO("Shutting down app.")
    if database.is_connected:
        await database.disconnect()
    
    