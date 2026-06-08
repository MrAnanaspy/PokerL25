from pydantic import BaseModel, Field, field_validator
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
