from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .db_secret import postgresql_password as db_password

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{db_password}@localhost/TodoApplicationDatabase'
# SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://root:{db_password}@127.0.0.1:3306/TodoApplicationDatabase'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})  # sqlite only
# engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
