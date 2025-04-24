from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import Optional, List


class TeamBase(SQLModel):
    name: str


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    name: Optional[str] = None


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationship を正しく定義
    players: List["Player"] = Relationship(
        sa_relationship=relationship(back_populates="team")
    )
