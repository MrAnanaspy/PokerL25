from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.dependency import get_current_user, get_db
from app.models import User
from app.schemas import GameRequest
from app.services import games as games_service

router = APIRouter()


@router.post("/game/create")
def create_game(
        game_request: GameRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return games_service.create_game(
        game=game_request,
        db=db,
        current_user=current_user,
    )


@router.get("/game")
def get_game(
        game_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return games_service.get_game(
        game_id=game_id,
        db=db,
        current_user=current_user,
    )


@router.get("/games")
def get_all_games(
        date_from: datetime | None = Query(None),
        date_to: datetime | None = Query(None),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return games_service.get_all_games(
        date_from=date_from,
        date_to=date_to,
        db=db,
        current_user=current_user,
    )


@router.post("/game/reg")
def reg_for_the_game(
        game_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return games_service.reg_for_the_game(
        game_id=game_id,
        db=db,
        current_user=current_user,
    )