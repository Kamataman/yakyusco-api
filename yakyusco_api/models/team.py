from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import Optional, List


class TeamBase(SQLModel):
    id: str = Field(
        default=None, primary_key=True, unique=True, regex=r"^[a-zA-Z0-9]{1,10}$"
    )
    team_name: str


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    pass


class TeamUpdate(SQLModel):
    team_name: Optional[str] = None


class Team(TeamBase, table=True):
    players: List["Player"] = Relationship(
        sa_relationship=relationship(back_populates="team")
    )
    game_results: List["GameResult"] = Relationship(back_populates="team")
