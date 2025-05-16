from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from models.team import (
    Team,
    TeamRead,
    TeamCreate,
    TeamUpdate,
)
from db import SessionDep
from auth import authorize_user, get_current_user, set_custom_claims

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
    team: TeamCreate, session: SessionDep, uid=Depends(get_current_user)
) -> TeamRead:
    db_team = Team.model_validate(team)

    # Firebaseカスタムクレームに追加
    set_custom_claims(uid, team.id)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.put("/teams/{team_id}", response_model=TeamRead)
def update_team(
    team_id: str,
    update_team: TeamUpdate,
    session: SessionDep,
    uid=Depends(get_current_user),
) -> TeamRead:
    authorize_user(uid, team_id)
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    player_data = update_team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(player_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team
