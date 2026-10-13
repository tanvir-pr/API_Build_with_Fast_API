from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:tAN1TS233333V@db.plekkfycogwdxyrbmmtd.supabase.co:5432/postgres'

connect_args = {'check_same_thread': False} if SQLALCHEMY_DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()
