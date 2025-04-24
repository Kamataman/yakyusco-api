from fastapi import APIRouter, HTTPException
from sqlmodel import select
# 順番にインポートする必要がある
from ..models.team import Team, TeamCreate, TeamRead
from ..models.player import Player, PlayerCreate, PlayerRead, PlayerReadWithTeam

from ..db import SessionDep

router = APIRouter()

@router.get("/players/", response_model=list[PlayerRead])
def read_players(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> list[PlayerRead]:
    players = session.exec(select(Player).offset(offset).limit(limit)).all()
    return players

@router.get("/players/{player_id}", response_model=PlayerRead)
def read_player(
    player_id: int,
    session: SessionDep,
) -> PlayerRead:
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("/players/", response_model=PlayerRead)
def create_player(
    player: PlayerCreate,
    session: SessionDep,
) -> PlayerRead:
    db_player = Player.model_validate(player)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player