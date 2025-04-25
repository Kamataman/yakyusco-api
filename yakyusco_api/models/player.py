from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import List, Optional


class PlayerBase(SQLModel):
    name: str
    number: str = Field(regex=r"^[0-9]{1,3}$")


class PlayerCreate(PlayerBase):
    team_id: str


class PlayerRead(PlayerBase):
    id: int


class PlayerReadWithTeam(PlayerRead):  # 新しいクラスを追加
    team: Optional["Team"] = None


class PlayerUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    team: Optional[str] = None
    position: Optional[str] = None


class Player(PlayerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: Optional[str] = Field(default=None, foreign_key="team.id")

    team: Optional["Team"] = Relationship(
        sa_relationship=relationship(back_populates="players")
    )
    batting_results: List["BattingResult"] = Relationship(
        back_populates="player",
    )
    pitching_results: List["PitchingResult"] = Relationship(
        back_populates="player",
    )
    atbat_results: List["AtbatResult"] = Relationship(
        back_populates="player",
    )
