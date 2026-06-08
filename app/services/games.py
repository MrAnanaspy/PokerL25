from datetime import datetime, UTC

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.repository import games as games_repository
from app.dependency import get_current_user
from app.models import User, Game
from app.schemas import GameRequest, GameResponse


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