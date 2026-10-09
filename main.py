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

# endpoints

# add question
@app.post("/questions")
def create_questions(question: Question, db: db_dependency):
  db_question = models.Questions(question=question.question_text)
  db.add(db_question) # prepares question to be saved
  db.commit() # saves question to db
  db.refresh(db_question) # updates object with  latest value stored in db

  for choice in question.choices:
    db_choice = models.Choices(choice=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
    db.add(db_choice)
  db.commit()

# retrieve questions
@app.get("/questions/{question_id}")
def get_question(question_id: int, db: db_dependency):
  result = db.query(models.Questions).filter(models.Questions.id == question_id).first()
  if not result:
    raise HTTPException(status_code=404, detail="Question not found")
  return result

# all choices for specific question
@app.get("/choices/{question_id}")
def get_choices(question_id: int, db: db_dependency):
  result = db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
  if not result:
    raise HTTPException(status_code=404, detail="Choices not found")
  return result