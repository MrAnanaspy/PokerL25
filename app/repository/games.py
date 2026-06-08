from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Game
from app.schemas import GameResponse


def create_game(game_datetime: datetime, quantity_user: int, db: Session) -> Game:
    game = Game(
        start_game=game_datetime,
        max_players=quantity_user,
    )
    db.add(game)
    db.flush()

    return game