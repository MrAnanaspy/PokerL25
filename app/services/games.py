from datetime import datetime, UTC

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.repository import games as games_repository
from app.dependency import get_current_user
from app.models import User, Game
from app.schemas import GameRequest, GameResponse, RegForTheGame, TimerCreateResponse, TimerResponse


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


def create_timer(game_id: int, db: Session, current_user: User) -> TimerCreateResponse:

    timer = games_repository.create_timer(
        game_id=game_id,
        db=db
    )
    db.commit()
    return TimerCreateResponse.model_validate(timer)


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


def cancel_reg_for_the_game(game_id: int, db: Session, current_user: User) -> str:

    if not games_repository.is_game_exist(db, game_id):
        raise HTTPException(
            status_code=404,
            detail=f"Game {game_id} not found"
        )

    if not games_repository.checking_game_registration(game_id=game_id, db=db, current_user=current_user.id):
        raise HTTPException(
            status_code=400,
            detail=f"The user {current_user.login} is not registered in the game {game_id}"
        )

    reg = games_repository.cancel_reg_for_the_game(
        game_id=game_id,
        db=db,
        current_user=current_user.id
    )
    db.commit()
    return f"The user {current_user.login} canceled in the game {game_id}"


def get_timer(game_id: int, db: Session, current_user: User) -> dict:

    if not games_repository.is_game_exist(db, game_id):
        raise HTTPException(
            status_code=404,
            detail=f"Game {game_id} not found"
        )

    game = games_repository.get_game(game_id=game_id, db=db)
    list_reg = 10
    # games_repository.get_all_reg_for_the_game(game_id, db)
    timer = games_repository.get_timer(game_id, db)

    total_chips = list_reg*timer.quantity_chips*1.5
    levels = round(timer.total_time/timer.level_duration)
    start_bb = 10
    final_bb = total_chips/30
    rate = (final_bb/start_bb)**(1/(levels-1))

    result: dict[int, int] = {}

    for i in range(levels + 1):
        bb = start_bb * (rate ** i)
        if bb < 200:
            bb = round(bb, -1)
        else:
            bb = round(bb, -2)

        result[int(i)] = bb

    return result