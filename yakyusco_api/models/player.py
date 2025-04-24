from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.orm import relationship
from typing import Optional


class PlayerBase(SQLModel):
    name: str
    number: str = Field(regex=r"^[0-9]{1,3}$")


class PlayerCreate(PlayerBase):
    pass


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
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    # Relationship を正しく定義
    team: Optional["Team"] = Relationship(
        sa_relationship=relationship(back_populates="players")
    )
