from enum import Enum
from operator import and_
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.dialects.postgresql import ARRAY, ENUM
from typing import Optional, List
from datetime import datetime


class WinloseEnum(Enum):
    WIN = "W"
    LOSE = "L"
    DRAW = "D"


class PositionEnum(Enum):
    DH = 0
    P = 1
    C = 2
    _1B = 3
    _2B = 4
    _3B = 5
    SS = 6
    LF = 7
    CF = 8
    RF = 9
    PH = 10
    PR = 11


class PicherResultEnum(Enum):
    WIN = "W"
    LOSE = "L"
    HOLD = "H"
    SAVE = "S"
    NOTHING = "-"


class GameResultBase(SQLModel):
    team_id: str = Field(foreign_key="team.id")
    is_ff: bool
    date: datetime=Field(sa_column=Column(DateTime(timezone=True)))
    bf_Team_name: str = Field(max_length=30)
    ff_Team_name: str = Field(max_length=30)
    winlose: WinloseEnum
    review: str = Field(max_length=300)
    place: str = Field(max_length=30)
    innings: int = Field(ge=0, lt=15)
    bf_runs: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    ff_runs: List[int] = Field(sa_column=Column(ARRAY(Integer)))
    bf_total_runs: int = Field(ge=0)
    ff_total_runs: int = Field(ge=0)
    is_X: bool


class GameResultCreate(GameResultBase):
    batting_results: List["BattingResultCreate"] = None
    pitching_results: List["PitchingResultCreate"] = None


class GameResultRead(GameResultBase):
    id: int


class GameResultUpdate(SQLModel):
    is_ff: Optional[bool] = None
    date: Optional[datetime] = None
    bf_Team_name: Optional[str] = Field(max_length=30, default=None)
    ff_Team_name: Optional[str] = Field(max_length=30, default=None)
    winlose: Optional[WinloseEnum] = None
    review: Optional[str] = Field(max_length=300, default=None)
    place: Optional[str] = Field(max_length=30, default=None)
    innings: Optional[int] = Field(ge=0, lt=15, default=None)
    bf_runs: Optional[List[int]] = Field(sa_column=Column(ARRAY(Integer)), default=None)
    ff_runs: Optional[List[int]] = Field(sa_column=Column(ARRAY(Integer)), default=None)
    bf_total_runs: Optional[int] = Field(ge=0, default=None)
    ff_total_runs: Optional[int] = Field(ge=0, default=None)
    is_X: Optional[bool] = None
    batting_results: List["BattingResultCreate"] = None
    pitching_results: List["PitchingResultCreate"] = None


class GameResultReadWithDetail(GameResultRead):
    batting_results: List["BattingResultRead"] = None
    pitching_results: List["PitchingResultRead"] = None


class GameResult(GameResultBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    team: Optional["Team"] = Relationship(back_populates="game_results")
    batting_results: List["BattingResult"] = Relationship(
        sa_relationship=relationship(
            back_populates="game_result",
            order_by=lambda: BattingResult.batting_order,
            cascade="all, delete-orphan",
        )
    )
    pitching_results: List["PitchingResult"] = Relationship(
        sa_relationship=relationship(
            back_populates="game_result",
            order_by=("PitchingResult.pitching_order"),
            cascade="all, delete-orphan",
        )
    )
    atbat_results: List["AtbatResult"] = Relationship(back_populates="game_result")


class BattingResultBase(SQLModel):
    batting_order: int  # 配列の順番にしたい
    batting_order_num: int
    rbi: int = Field(ge=0)
    runs: int = Field(ge=0)
    steels: int = Field(ge=0)
    position: List[PositionEnum] = Field(sa_column=Column(ARRAY(ENUM(PositionEnum))))


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
    innings: int = Field(ge=0)
    pitchs: int = Field(ge=0)
    batters: int = Field(ge=0)
    hits: int = Field(ge=0)
    homeruns: int = Field(ge=0)
    strikeouts: int = Field(ge=0)
    walks: int = Field(ge=0)
    hit_by_pitch: int = Field(ge=0)
    balks: int = Field(ge=0)
    runs: int = Field(ge=0)
    earned_runs: int = Field(ge=0)
    result: PicherResultEnum
    pitching_order: int  # 配列の順番にしたい


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
    position: Optional[int] = Field(default=None)
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
