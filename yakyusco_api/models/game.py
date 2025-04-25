from operator import and_
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.dialects.postgresql import ARRAY
from typing import Optional, List
from datetime import datetime


class GameResultBase(SQLModel):
    team_id: str = Field(foreign_key="team.id")
    is_ff: bool
    date: datetime
    bf_Team_name: str
    ff_Team_name: str
    winlose: str
    review: str
    place: str
    innings: int
    bf_runs: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    ff_runs: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    bf_total_runs: int
    ff_total_runs: int
    is_X: bool


class GameResultCreate(GameResultBase):
    batting_results: List["BattingResultCreate"] = None
    pitching_results: List["PitchingResultCreate"] = None


class GameResultRead(GameResultBase):
    id: int
    batting_results: List["BattingResultRead"] = None
    pitching_results: List["PitchingResultRead"] = None


class GameResult(GameResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    team: Optional["Team"] = Relationship(back_populates="game_results")
    batting_results: List["BattingResult"] = Relationship(
        sa_relationship=relationship(
            back_populates="game_result", order_by=lambda: BattingResult.batting_order
        )
    )
    pitching_results: List["PitchingResult"] = Relationship(
        sa_relationship=relationship(
            back_populates="game_result",
            order_by=("PitchingResult.pitching_order"),
        )
    )
    atbat_results: List["AtbatResult"] = Relationship(back_populates="game_result")


class BattingResultBase(SQLModel):
    player_number: str
    player_name: str
    batting_order: int
    batting_order_num: int
    rbi: int
    runs: int
    steels: int
    position: List[int] = Field(sa_column=Column(ARRAY(Integer)))


class BattingResultCreate(BattingResultBase):
    player_id: int
    atbat_results: List["AtbatResultCreate"] = None


class BattingResultRead(BattingResultBase):
    player_id: int
    atbat_results: List["AtbatResultRead"] = None


class BattingResult(BattingResultBase, table=True):
    gameresult_id: Optional[int] = Field(
        default=None, foreign_key="gameresult.id", primary_key=True
    )
    player_id: Optional[int] = Field(foreign_key="player.id", primary_key=True)

    # Relationships
    game_result: Optional["GameResult"] = Relationship(back_populates="batting_results")
    player: Optional["Player"] = Relationship(back_populates="batting_results")
    atbat_results: List["AtbatResult"] = Relationship(
        sa_relationship=relationship(
            primaryjoin=lambda: and_(
                foreign(AtbatResult.gameresult_id) == BattingResult.gameresult_id,
                foreign(AtbatResult.player_id) == BattingResult.player_id,
            ),
            # back_populates="batting_result",
            order_by="AtbatResult.num_atbat",
        )
    )


class PitchingResultBase(SQLModel):
    player_number: str
    player_name: str
    innings: int
    pitchs: int
    batters: int
    hits: int
    homeruns: int
    strikeouts: int
    walks: int
    hit_by_pitch: int
    balks: int
    runs: int
    earned_runs: int
    result: str
    pitching_order: int


class PitchingResultCreate(PitchingResultBase):
    player_id: int


class PitchingResultRead(PitchingResultBase):
    player_id: int


class PitchingResult(PitchingResultBase, table=True):
    gameresult_id: int = Field(
        default=None, foreign_key="gameresult.id", primary_key=True
    )
    player_id: int = Field(default=None, foreign_key="player.id", primary_key=True)

    # Relationships
    game_result: Optional["GameResult"] = Relationship(
        back_populates="pitching_results"
    )
    player: Optional["Player"] = Relationship(back_populates="pitching_results")


class AtbatResultBase(SQLModel):
    inning: int
    result: str
    position: int
    is_scpos: bool


class AtbatResultCreate(AtbatResultBase):
    pass


class AtbatResultRead(AtbatResultBase):
    pass


class AtbatResult(AtbatResultBase, table=True):
    num_atbat: Optional[int] = Field(default=None, primary_key=True)
    gameresult_id: int = Field(
        default=None, foreign_key="gameresult.id", primary_key=True
    )
    player_id: Optional[int] = Field(
        default=None, foreign_key="player.id", primary_key=True
    )

    # # Relationships
    game_result: Optional["GameResult"] = Relationship(back_populates="atbat_results")
    player: Optional["Player"] = Relationship(back_populates="atbat_results")
