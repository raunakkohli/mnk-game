# TIC TAC TOE - Backend Application

### _The most famous version of a `mnk` Game_


- [About game](#about-game)
- [About application](#about-application)
  - [Scope](#scope)
  - [APIs](#apis)
    - [Create New Game](#create-new-game)
      - [Endpoint](#endpoint)
      - [Request Payload Parameters](#request-payload-parameters)
      - [Request sample](#request-sample)
      - [Response Payload Parameters](#response-payload-parameters)
      - [Response sample](#response-sample)
      - [Exceptions](#exceptions)
    - [Make New Move](#make-new-move)
      - [Endpoint](#endpoint-1)
      - [Request Payload Parameters](#request-payload-parameters-1)
      - [Request sample](#request-sample-1)
      - [Response Payload Parameters](#response-payload-parameters-1)
      - [Response sample](#response-sample-1)
      - [Exceptions](#exceptions-1)
- [Project structure](#project-structure)
- [Setup](#setup)
- [Developer docs](#developer-docs)


## About game

Tic-Tac-Toe is 2D game played by two players on a 3x3 board, generally with `x` and `o` as their respective game markers. 
The rules are simple, where the players alternately place the marks `x` and `o` in one of the nine spaces in the grid, and the first one to get 3 markers in a row/column/diagonal wins.
The game can be generalized to an `m,n,k-game`, in which two players alternate placing stones of their own color on an m-by-n board with the goal of getting k of their own color in a line. Tic-tac-toe is the mnk-game where m,n,k all are 3.
[read more @ wiki](https://en.wikipedia.org/wiki/Tic-tac-toe)


## About application 

This is a backend only application, which is built using `python` + `fastAPI` + `postgres`. 

### Scope

For scope it assumes the scenario where:
-  Player(s) use a single client to play a game.
    > Multiple instances of such client can interact with the backend app, since the implementation supports concurrent games.
-  There will be only 2 players at the max in a game.
-  A game could be of 2 types:
    1. Single player (versus the computer)
    2. Two player (2 people playing on the same client in turns)
-  Players play with `x` and `o` as their pawns (pieces).
    > The implementation has a provision to override this by an optional configuration and custom pawns can be chosen.
-  Player that plays with `x` will make the first move.
    > The implementation has a provision to override this by an optional configuration and provide a different starting pawn.
-  Game outcomes can be that either player has won or it ends in a tie/draw. The game is officially concluded once it reaches these outcomes, until which time it will be in progress.
-  Player moves are recorded to support move-history feature.
-  The client would bind API response information to UI elements in a reactive manner, so all required data is to be passed.
-  There is no Player-login/Saved-user scenario at present. Hence there is no user data persistence or authentication of same.
    > However, game persistence is present and supported (which is linked with the respective game id ).

### APIs

There are 2 main APIs that can be used by client to interact with backend app, in order to play the game.

#### Create New Game

The first API that would be invoked is to create a new game. It expects to provided with game configuration, and responds with initialised game and a unique game id which is to be used for all future communications pertaining to that game.

##### Endpoint

> `POST` host-url`/tictactoe`

##### Request Payload Parameters

- `mode`: Corresponds to game mode. It can take values: `SINGLE_PLAYER` or `TWO_PLAYER`
- `player_1`: Corresponds to player 1 pawn.
- `player_2` [optional]: Corresponds to player 1 pawn.
    >For `SINGLE_PLAYER` mode only player_1 is needed, and player 2 is auto assigned. 
    For `TWO_PLAYER` mode if player 2 is not provided then it will be auto assigned based on starting pawn configuration and default pawns (primary:`x`, secondary: `o`).
- `starting_pawn` [optional]: Corresponds to override for starting pawn. 
    >Either player 1 or player 2 must be assigned this. 
    If player 2 pawn is not provided and player 1 pawn is not the starting pawn, then player 2 will automatically be assigned that.

##### Request sample

```json
{
    "mode": "TWO_PLAYER",
    "player_1": "x",
    "player_2": "o"
}
```

##### Response Payload Parameters

- `game_id`: Corresponds to a unique game identifier for reference.
- `game_board`: 3x3 matrix which can be bound to UI for display.
- `game_status`: This tells the current game status. It can be of the following values - {`IN_PROGRESS`, `PLAYER_1_WINS`, `PLAYER_2_WINS`, `TIED`}. 
- `player_1`: Corresponds to player 1 pawn.
- `player_2`: Corresponds to player 2 pawn.
- `player_turn`: Corresponds to player pawn which needs to play.

##### Response sample

```json
{
    "game_id": "xyz-abc2-1001-2ab1-zxcvbb",
    "game_board":  [["-","-","-"],
                    ["-","-","-"],
                    ["-","-","-"]],
    "game_status": "IN_PROGRESS",
    "player_1": "x",
    "player_2": "o",
    "player_turn": "x"
}
```

##### Exceptions

These scenarios would be validated and throw exception:
- Invalid Game Mode passed in request body.
- Mandatory parameter(s) not passed in request body.
- Same pawn markers passed for both player_1 and player_2.
- Starting pawn not respected.
    > Ex1: passing `a` and `b` but default starting pawn is `x`.  
    > Ex2: passing `x` and `o` but providing override of `starting_pawn` as `m`.


#### Make New Move

This API that would be invoked to make a new move by player whose turn it is to play. It expects to be provided with game id, pawn and location on board which needs to be marked.

##### Endpoint

> `POST` host-url`/tictactoe/move`

##### Request Payload Parameters

- `game_id`: corresponds the game reference identifier that was given when the game was created.
- `pawn`: Corresponds to player pawn.
- `row`: Corresponds to row on board.
- `column`: Corresponds to column on board.


##### Request sample

```json
{
    "game_id": "xyz-abc2-1001-2ab1-zxcvbb",
    "pawn": "x",
    "row": 0,
    "column": 1
}
```

##### Response Payload Parameters

- `game_id`: Corresponds to a unique game identifier.
- `game_board`: 3x3 matrix which can be bound to UI for display.
- `game_status`: This tells the current game status. It can be of the following values - {`IN_PROGRESS`, `PLAYER_1_WINS`, `PLAYER_2_WINS`, `TIED`}. 
- `player_1`: Corresponds to player 1 pawn.
- `player_2`: Corresponds to player 2 pawn.
- `player_turn`: Corresponds to player pawn which needs to play.
- `moves`: list of moves made in the game.


##### Response sample

```json
{
    "game_id": "xyz-abc2-1001-2ab1-zxcvbb",
    "game_board":  [["x","-","-"],
                    ["-","-","-"],
                    ["-","-","-"]],
    "game_status": "IN_PROGRESS",
    "player_1": "x",
    "player_2": "o",
    "player_turn": "o",
    "moves": [
        {
            "pawn": "x",
            "row": 2,
            "column": 2,
            "created": "05/11/2021, 20:48:16:875898"
        }
    ]
}
```

##### Exceptions

These scenarios would be validated and throw exception:

- Missing mandatory parameter(s).
- Trying to make a move with invalid game id.
- Trying to make a move when game is already concluded.
- Trying to make a move on a spot which is not vacant or out of bounds.
- Trying to make a move out of turn.

## Project structure
- `mnk` : main package for m-n-k game
    - `mnk.exceptions`: all custom exceptions 
    - `mnk.helpers`: helper methods collection
    - `mnk.models`: service, API and DB data models
    - `mnk.repository`: repository of games in memory (cache module)
    - `mnk.routers`: API router/controllers
    - `mnk.svc`: game service logic
    - `mnk.app.py`: main application run file
    - `mnk.database.py`: database init file
    - `mnk.config.py`: env config file
- `tests`: unit tests
- `POSTMAN`: integration scenario tests in postman collection
- `DOCS`: other documentation related to design and development of project
- `docker-compose.yml`: docker config file
- `Dockerfile`: docker file for initialising web module
- `requirements.txt`: dependencies of the project
- `README.md`: you are here!


## Setup
Follow these steps to get the app running on your machine.
1. Make sure you have [Docker](https://docs.docker.com/get-docker/) installed, then start it up.
2. Clone/download this repository.
3. Head to the root of the project. (`cd` to root)
4. Open terminal at that location.
5. Run the following command to compose: 
```sh 
docker-compose up -d --build
```
**NOTE:** Alternatively, you can also run it in 2 steps if you prefer to break it down into first composing the images, and then running them in containers as a second step
```sh 
docker-compose build
docker-compose up -d
```
6. You can head over to docker app on your machine to confirm that the web and db modules are up and running on your localhost (`http://localhost:8008`).
7. **AND DONE!** That was easy right? We now have the back end app running in our local machine, so you can start interacting with it now. 

> If you want to interact with the APIs feel free to use the postman collection as reference. If you don't already have postman, you can get it from [here](https://www.postman.com/downloads/).

> Once you are done with the app, you can stop the container and delete the postgres data by executing the following commands:
```sh 
docker-compose down
docker volume rm $(docker volume ls -q)
```


## Developer Docs

For more documentation on development and design look [here](./DOCS/development_doc.md)
