from fastapi import APIRouter, HTTPException
from sqlmodel import Integer, cast, select
from ..models.player import (
    Player,
    PlayerCreate,
    PlayerRead,
    PlayerUpdate,
)
from ..db import SessionDep

router = APIRouter()


@router.get("/teams/{team_id}/players/", response_model=list[PlayerRead])
def read_players(
    team_id: str,
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> list[PlayerRead]:
    players = session.exec(
        select(Player)
        .where(Player.team_id == team_id)
        .order_by(cast(Player.number, Integer))
        .offset(offset)
        .limit(limit)
    ).all()
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


@router.put("/players/{player_id}", response_model=PlayerRead)
def update_player(
    player_id: int,
    update_player: PlayerUpdate,
    session: SessionDep,
) -> PlayerRead:
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_data = update_player.model_dump(exclude_unset=True)
    db_player.sqlmodel_update(player_data)
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player


@router.delete("/players/{player_id}")
def delete_player(player_id: int, session: SessionDep):
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    session.delete(db_player)
    session.commit()
    return {"message": "Player deleted successfully"}
