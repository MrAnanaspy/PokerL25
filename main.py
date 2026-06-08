from fastapi import FastAPI
from app.api.v1.games import router as game_router
from app.api.v1.users import router as user_router
from app.database import Base, engine


app = FastAPI()

app.include_router(game_router, prefix="/api/v1", tags=["games"])
app.include_router(user_router, prefix="/api/v1", tags=["users"])


Base.metadata.create_all(bind=engine)