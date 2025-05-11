from fastapi import APIRouter, HTTPException
from sqlmodel import select

from models.team import (
    Team,
    TeamRead,
    TeamCreate,
)
from db import SessionDep

router = APIRouter()


@router.get("/teams/", response_model=list[TeamRead])
def read_teams(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> list[TeamRead]:
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamRead)
def read_team(
    team_id: str,
    session: SessionDep,
) -> TeamRead:
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.post("/teams/", response_model=TeamRead)
def create_team(
    team: TeamCreate,
    session: SessionDep,
) -> TeamRead:
    db_team = Team.model_validate(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team
