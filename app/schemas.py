from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime


class UserRequest(BaseModel):
    login: str = Field(..., max_length=127)


class UserResponse(UserRequest):
    model_config = {"from_attributes": True}

    id: int


class GameRequest(BaseModel):

    game_datetime: datetime
    quantity_users: int

    @field_validator("quantity_users")
    def quantity_users_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity users must be positive")
        return v


class GameResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    start_game: datetime
    max_players: int


class RegForTheGame(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    game_id: int
    user_id: int
    reg_datetime: datetime


class TimerCreateResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    game_id: int
    started_at: datetime | None
    paused_at: datetime | None

    quantity_chips: int
    total_time: int
    level_duration: int

    @field_validator("total_time")
    def total_time_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Total time must be positive")
        return v

    @field_validator("quantity_chips")
    def quantity_chips_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Quantity CHIPS must be positive")
        return v

    @field_validator("level_duration")
    def level_duration_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Level duration must be positive")
        return v


class TimerResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    game_id: int
    started_at: datetime | None
    paused_at: datetime | None


class PlayOrPauseTimerResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    game_id: int
    started_at: datetime | None
    paused_at: datetime | None
