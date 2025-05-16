from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import Optional, List


class TeamBase(SQLModel):
    id: str = Field(
        default=None,
        primary_key=True,
        unique=True,
        schema_extra={"pattern": r"^[a-z0-9]+$"},
        max_length=20,
    )
    team_name: str = Field(max_length=30)
    description: str = Field(max_length=1000)


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    pass


class TeamUpdate(SQLModel):
    team_name: Optional[str] = None
    description: Optional[str] = None


class Team(TeamBase, table=True):
    players: List["Player"] = Relationship(
        sa_relationship=relationship(back_populates="team")
    )
    game_results: List["GameResult"] = Relationship(back_populates="team")
