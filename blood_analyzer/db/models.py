"""
Module is used for crating SQL models. Each class represents separate tables in database.
Login manager decorator allows to make login for user.
"""

# PSL
from os import getenv

from sqlalchemy import ForeignKey, UniqueConstraint
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from blood_analyzer import _DB, _LOGIN_MANAGER

_SECRET_KEY = getenv("SECRET_KEY")


@_LOGIN_MANAGER.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(_DB.Model, UserMixin):
    """
    Model for creating table user in database.
    """
    id = _DB.Column(_DB.Integer, primary_key=True)
    username = _DB.Column(_DB.String(20), unique=True, nullable=False)
    email = _DB.Column(_DB.String(120), unique=True, nullable=False)
    password = _DB.Column(_DB.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(_SECRET_KEY, expires_sec)
        return s.dumps({"user.id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(_SECRET_KEY)
        try:
            user_id = s.loads(token)["user.id"]
        except:
            return None
        return User.query.get(user_id)


class Patients(_DB.Model):
    """
    Model for creating table patients in database.
    """
    id = _DB.Column(_DB.Integer, primary_key=True)
    patient_id = _DB.Column(_DB.String(20), unique=True, nullable=False)
    birth_date = _DB.Column(_DB.String(20), nullable=False)
    results = _DB.relationship("Results")


class Results(_DB.Model):
    """
    Model for creating table results in database.
    """
    id = _DB.Column(_DB.Integer, primary_key=True)
    patient_id = _DB.Column(
        _DB.String(20), ForeignKey("patients.patient_id"), nullable=False
    )
    LAB_CODE = _DB.Column(_DB.String(20), nullable=False)
    DATE = _DB.Column(_DB.Date(), nullable=False)
    WBC = _DB.Column(_DB.Float, nullable=True)
    NEU = _DB.Column(_DB.Float, nullable=True)
    LYM = _DB.Column(_DB.Float, nullable=True)
    MONO = _DB.Column(_DB.Float, nullable=True)
    BASO = _DB.Column(_DB.Float, nullable=True)
    EOS = _DB.Column(_DB.Float, nullable=True)
    RBC = _DB.Column(_DB.Float, nullable=True)
    HCT = _DB.Column(_DB.Float, nullable=True)
    HGB = _DB.Column(_DB.Float, nullable=True)
    MCV = _DB.Column(_DB.Float, nullable=True)
    MCH = _DB.Column(_DB.Float, nullable=True)
    MCHC = _DB.Column(_DB.Float, nullable=True)
    PLT = _DB.Column(_DB.Float, nullable=True)
    MPV = _DB.Column(_DB.Float, nullable=True)
    PCT = _DB.Column(_DB.Float, nullable=True)
    RET = _DB.Column(_DB.Float, nullable=True)
    RET_PERCENT = _DB.Column("RET%", _DB.Float, nullable=True)
    IRF = _DB.Column(_DB.Float, nullable=True)
    RDW = _DB.Column(_DB.Float, nullable=True)
    RDW_SD = _DB.Column("RDW-SD", _DB.Float, nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "LAB_CODE", "DATE", "WBC", "PLT", "HGB", "MCH", "MCHC", "MCV", "HCT", "RBC"
        ),
    )
