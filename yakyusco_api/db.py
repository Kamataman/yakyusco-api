from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from decouple import config

# 環境変数から設定を読み込む
DATABASE_URL = config("DATABASE_URL")
ECHO_LOG = config("ECHO_LOG", cast=bool, default=True)

engine = create_engine(DATABASE_URL, echo=ECHO_LOG)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
