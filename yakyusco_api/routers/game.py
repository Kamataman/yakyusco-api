from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..models.game import (
    GameResult,
    GameResultRead,
    GameResultCreate,
    BattingResult,
    PitchingResult,
    AtbatResult,
)

from ..db import SessionDep

router = APIRouter()


@router.get("/gameresults/", response_model=list[GameResultRead])
def read_teams(
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> list[GameResultRead]:
    teams = session.exec(select(GameResult).offset(offset).limit(limit)).all()
    return teams


@router.get("/gameresults/{gameresult_id}", response_model=GameResultRead)
def read_team(
    gameresult_id: str,
    session: SessionDep,
) -> GameResultRead:
    gameresult = session.get(GameResult, gameresult_id)
    if not gameresult:
        raise HTTPException(status_code=404, detail="GameResult not found")
    return gameresult


@router.post("/gameresults/", response_model=GameResultRead)
def create_team(
    gameresult: GameResultCreate,
    session: SessionDep,
) -> GameResultRead:

    # BattingResult の変換と追加
    if gameresult.batting_results:
        validated_batting_results = []
        for batting_result in gameresult.batting_results:
            validated_atbat_results = []
            for i, atbat_result in enumerate(batting_result.atbat_results):
                _a = AtbatResult.model_validate(atbat_result)
                _a.num_atbat = i + 1
                _a.player_id = batting_result.player_id
                validated_atbat_results.append(_a)
            batting_result.atbat_results = validated_atbat_results
            validated_batting_results.append(
                BattingResult.model_validate(batting_result)
            )
        gameresult.batting_results = validated_batting_results

    # PitchingResult の変換と追加
    if gameresult.pitching_results:
        gameresult.pitching_results = list(
            map(lambda x: PitchingResult.model_validate(x), gameresult.pitching_results)
        )

    db_gameresult = GameResult.model_validate(gameresult)
    session.add(db_gameresult)
    session.commit()
    session.refresh(db_gameresult)
    return db_gameresult
