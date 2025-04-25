from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager

from .db import create_db_and_tables
from .routers import player, team,game


@asynccontextmanager
async def lifespan(app: FastAPI):
    # init
    create_db_and_tables()
    yield
    # close


app = FastAPI(lifespan=lifespan)
app.include_router(player.router)
app.include_router(team.router)
app.include_router(game.router)


@app.get("/")
async def read_main():
    return {"msg": "Hello Yakyusco API !!"}


origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    print(exc.orig)
    return JSONResponse(
        status_code=400,
        content={"detail": "Integrity error occurred"},
    )
