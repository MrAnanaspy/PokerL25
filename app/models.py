from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_game: Mapped[datetime]
    max_players: Mapped[int]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    tg_id: Mapped[str | None] = mapped_column(unique=True)
    rating: Mapped[Decimal] = mapped_column(default=1000.0)


class RegistrationForTheGame(Base):
    __tablename__ = "registration_for_the_game"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    reg_datetime: Mapped[datetime] = mapped_column(default=lambda: datetime.now())


class Timer(Base):
    __tablename__ = "Timer"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False, unique=True)
    started_at: Mapped[datetime | None] = mapped_column(default=None)
    paused_at: Mapped[datetime | None] = mapped_column(default=None)

    # Config timer
    quantity_chips: Mapped[int] = mapped_column(default=1000)
    total_time: Mapped[int] = mapped_column(default=180)
    level_duration: Mapped[int] = mapped_column(default=20)
