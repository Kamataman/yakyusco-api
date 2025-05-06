from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..models.game import (
    GameResult,
    GameResultRead,
    GameResultReadWithDetail,
    GameResultCreate,
    GameResultUpdate,
    BattingResult,
    PitchingResult,
    AtbatResult,
)

from ..db import SessionDep

router = APIRouter()


@router.get("/teams/{team_id}/gameresults/", response_model=list[GameResultRead])
def read_gameresults(
    team_id: str,
    session: SessionDep,
    offset: int = 0,
    limit: int = 100,
) -> list[GameResultRead]:
    teams = session.exec(
        select(GameResult)
        .where(GameResult.team_id == team_id)
        .offset(offset)
        .limit(limit)
    ).all()
    return teams


@router.get("/gameresults/{gameresult_id}", response_model=GameResultReadWithDetail)
def read_gameresult(
    gameresult_id: str,
    session: SessionDep,
) -> GameResultReadWithDetail:
    db_gameresult = session.get(GameResult, gameresult_id)
    if not db_gameresult:
        raise HTTPException(status_code=404, detail="GameResult not found")
    return db_gameresult


@router.post("/gameresults/", response_model=GameResultReadWithDetail)
def create_gameresult(
    gameresult: GameResultCreate,
    session: SessionDep,
) -> GameResultReadWithDetail:

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


@router.put("/gameresults/{gameresult_id}", response_model=GameResultReadWithDetail)
def update_gameresult(
    gameresult_id: int,
    update_gameresult: GameResultUpdate,
    session: SessionDep,
) -> GameResultReadWithDetail:
    db_gameresult = session.get(GameResult, gameresult_id)
    if not db_gameresult:
        raise HTTPException(status_code=404, detail="Gameresult not found")

    # BattingResult の変換と追加
    if update_gameresult.batting_results:
        validated_batting_results = []
        for batting_result in update_gameresult.batting_results:
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
        update_gameresult.batting_results = validated_batting_results

    # PitchingResult の変換と追加
    if update_gameresult.pitching_results:
        update_gameresult.pitching_results = list(
            map(
                lambda x: PitchingResult.model_validate(x),
                update_gameresult.pitching_results,
            )
        )

    gameresult_data = update_gameresult.model_dump(exclude_unset=True)
    db_gameresult.sqlmodel_update(gameresult_data)
    session.add(db_gameresult)
    session.commit()
    session.refresh(db_gameresult)
    return db_gameresult


@router.delete("/gameresults/{gameresult_id}")
def delete_gameresult(gameresult_id: int, session: SessionDep):
    db_gameresult = session.get(GameResult, gameresult_id)
    if not db_gameresult:
        raise HTTPException(status_code=404, detail="Gameresult not found")
    session.delete(db_gameresult)
    session.commit()
    return {"message": "Gameresult deleted successfully"}
