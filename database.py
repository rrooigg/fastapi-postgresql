from sqlalchemy import create_engine # connects db with fastapi application
from sqlalchemy.orm import sessionmaker # creates factory for db sessions(sessions mean db operations i.e adding etc)
from sqlalchemy.ext.declarative import declarative_base # to create a base class to define db tables
import os

# 1. create db in postgresql

# 2. db url
DATABASE_URL = os.getenv("DATABASE_URL")

# 3. create connection
engine = create_engine(DATABASE_URL)

# 4. sessionmaker -> creates db sessions
# bind=engine -> which db to use
# autoflush=False -> prevents sqlalchemy from automatically flushing when there's changes made (flush -> forcing any data modification temporarily held in ram/cache to be permanently written in hard disk)
# autocommit=False -> prevents automatically saving changes 
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 5. create base class
Base = declarative_base()
