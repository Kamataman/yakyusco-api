from fastapi import APIRouter
from sqlmodel import Integer, select
from models.player import Player
from models.game import BattingResult, AtbatResult, PitchingResult
from models.stats import BattingStatsRead, PitchingStatsRead
from db import SessionDep

router = APIRouter()


@router.get("/teams/{team_id}/stats/batting", response_model=list[BattingStatsRead])
def get_batting_stats(team_id: str, session: SessionDep) -> list[BattingStatsRead]:
    players = session.exec(select(Player).where(Player.team_id == team_id)).all()

    battingStats = []
    for player in players:
        battingStats.append(
            BattingStatsRead(
                player.number,
                player.name,
                session.exec(
                    select(BattingResult).where(BattingResult.player_id == player.id)
                ).all(),
                session.exec(
                    select(AtbatResult).where(AtbatResult.player_id == player.id)
                ).all(),
            )
        )

    return battingStats


@router.get("/teams/{team_id}/stats/pitching", response_model=list[PitchingStatsRead])
def get_pitching_stats(team_id: str, session: SessionDep) -> list[PitchingStatsRead]:
    players = session.exec(select(Player).where(Player.team_id == team_id)).all()

    pitchingStats = []
    for player in players:
        pitchingStats.append(
            PitchingStatsRead(
                player.number,
                player.name,
                session.exec(
                    select(PitchingResult).where(PitchingResult.player_id == player.id)
                ).all(),
            )
        )

    return pitchingStats
