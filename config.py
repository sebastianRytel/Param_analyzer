from dataclasses import dataclass
from os import getenv


@dataclass
class Config:
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///static/site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY: str = getenv("SECRET_KEY", "PUT YOUR SECRET KEY!")
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
