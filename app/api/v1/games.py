from fastapi import APIRouter, Depends
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