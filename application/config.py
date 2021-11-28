import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = None

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_dir")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(SQLITE_DB_DIR, "flashCardDb.sqlite3")
    DEBUG = True
    JWT_SECRET_KEY = "fsh3423hoi3"
    ACCESS_EXPIRES = timedelta(hours=1)
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    # os.environ.get('SECRET_KEY')
    SECRET_KEY = "fsh3423hoi3"
    SECURITY_PASSWORD_HASH = "bcrypt"
    # os.environ.get('PASSWORD')
    SECURITY_PASSWORD_SALT = "lifesucks"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None

class ProdDevConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_dir")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(SQLITE_DB_DIR, "prodFlashCardDb.sqlite3")
    DEBUG = False
    # os.environ.get('SECRET_KEY')
    SECRET_KEY = "fsh3423hoi3"
    SECURITY_PASSWORD_HASH = "bcrypt"
    # os.environ.get('PASSWORD')
    SECURITY_PASSWORD_SALT = "lifesucks"
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None

