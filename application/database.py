from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

enginer = None
Base = declarative_base()
db = SQLAlchemy()
