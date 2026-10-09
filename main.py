from fastapi import FastAPI, HTTPException, Depends 
# Depends for dependency injection(an object receives other objects/services from external source instead of creating/managing them itself)
from pydantic import BaseModel
from typing import Annotated 

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# creates tables in db based on models defined
models.Base.metadata.create_all(bind=engine)

class Choice(BaseModel):
  choice_text: str
  is_correct: bool

class Question(BaseModel):
  question_text: str
  choices: list[Choice]

# connect app with db
def get_db():
  db = SessionLocal()
  try:
    yield db # yield -> gives db to whoever requested it i.e fastapi endpoint.
  finally:
    db.close()

# annotaions. a shortcut(to request db session) instead of using it in every shortcut
# Session -> value expected, Depends(get_db) -> how to obtain the value
# variable name(db_dependency) can also be DBSession/DatabaseSession
db_dependency = Annotated[Session, Depends(get_db)]