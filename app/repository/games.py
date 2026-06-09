from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Game, User, RegistrationForTheGame, Timer
from app.schemas import GameResponse


def create_game(game_datetime: datetime, quantity_user: int, db: Session) -> Game:
    game = Game(
        start_game=game_datetime,
        max_players=quantity_user,
    )
    db.add(game)
    db.flush()

    return game


def create_timer(game_id: int, db: Session) -> Game:
    timer = Timer(
        game_id=game_id,
    )
    db.add(timer)
    db.flush()

    return timer


def get_game(game_id: int, db: Session) -> Game:
    game = db.query(Game).filter(Game.id == game_id).scalar()
    return game


def is_game_exist(db: Session, game_id: int) -> bool:
    return db.query(Game).filter(Game.id == game_id).first() is not None


def get_all_games(date_from: datetime, date_to: datetime, db: Session) -> list[Game]:
    query = db.query(Game)

    if date_from:
        query = query.filter(Game.start_game >= date_from)

    if date_to:
        query = query.filter(Game.start_game <= date_to)

    return query.all()


def reg_for_the_game(game_id: int, db: Session, current_user: int) -> RegistrationForTheGame:
    reg = RegistrationForTheGame(
        game_id=game_id,
        user_id=current_user,
    )
    db.add(reg)
    db.flush()

    return reg


def get_all_reg_for_the_game(game_id: int, db: Session) -> list[RegistrationForTheGame]:
    return db.query(RegistrationForTheGame).filter(RegistrationForTheGame.game_id == game_id).all()


def checking_game_registration(game_id: int, db: Session, current_user: int) -> bool:

    return db.query(RegistrationForTheGame).filter(
        RegistrationForTheGame.game_id == game_id,
        RegistrationForTheGame.user_id == current_user
    ).first() is not None


def cancel_reg_for_the_game(game_id: int, db: Session, current_user: int) -> RegistrationForTheGame:
    reg = db.query(RegistrationForTheGame).filter(RegistrationForTheGame.game_id == game_id).scalar()
    db.delete(reg)
    db.flush()
    return reg


def get_timer(game_id: int, db: Session) -> Timer:
    timer = db.query(Timer).filter(Timer.game_id == game_id).scalar()
    return timer
