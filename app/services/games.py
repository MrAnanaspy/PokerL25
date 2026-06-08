from datetime import datetime, UTC

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.repository import games as games_repository
from app.dependency import get_current_user
from app.models import User, Game
from app.schemas import GameRequest, GameResponse, RegForTheGame


def create_game(game: GameRequest, db: Session, current_user: User) -> GameResponse:
    if game.game_datetime < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="The game time cannot be set in the past")

    game = games_repository.create_game(
        game_datetime=game.game_datetime,
        quantity_user=game.quantity_users,
        db=db
    )
    db.commit()
    return GameResponse.model_validate(game)


def get_game(game_id: int, db: Session, current_user: User) -> GameResponse:

    if not games_repository.is_game_exist(db, game_id):
        raise HTTPException(
            status_code=404,
            detail=f"Game {game_id} not found"
        )

    game = games_repository.get_game(
        game_id=game_id,
        db=db
    )
    return GameResponse.model_validate(game)


def get_all_games(date_from: datetime, date_to: datetime, db: Session, current_user: User) -> list[GameResponse]:

    games = games_repository.get_all_games(
        date_from=date_from,
        date_to=date_to,
        db=db,
    )

    result = []
    for game in games:
        result.append(GameResponse.model_validate(game))

    return result


def reg_for_the_game(game_id: int, db: Session, current_user: User) -> RegForTheGame:

    if not games_repository.is_game_exist(db, game_id):
        raise HTTPException(
            status_code=404,
            detail=f"Game {game_id} not found"
        )

    list_reg = games_repository.get_all_reg_for_the_game(game_id, db)
    game = games_repository.get_game(game_id, db)
    if len(list_reg) >= game.max_players:
        raise HTTPException(
            status_code=400,
            detail=f"All seats in the game {game_id} are already taken"
        )

    if games_repository.checking_game_registration(game_id=game_id, db=db, current_user=current_user.id):
        raise HTTPException(
            status_code=400,
            detail=f"The user {current_user.login} is already registered in the game {game_id}"
        )

    reg = games_repository.reg_for_the_game(
        game_id=game_id,
        db=db,
        current_user=current_user.id
    )

    db.commit()
    return RegForTheGame.model_validate(reg)