"""
Models for Customer Accounts
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

db = SQLAlchemy()


def init_db(app):
    """Initializes the SQLAlchemy app"""
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)
    with app.app_context():
        db.create_all()


class Account(db.Model):
    """Class that represents a Customer Account"""

    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    address = db.Column(db.String(256), nullable=True)
    phone_number = db.Column(db.String(32), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f"<Account {self.name} id={self.id}>"

    def serialize(self):
        """Serializes an Account into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "address": self.address,
            "phone_number": self.phone_number,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }

    def deserialize(self, data):
        """Deserializes an Account from a dictionary"""
        try:
            self.name = data["name"]
            self.email = data["email"]
            self.address = data.get("address")
            self.phone_number = data.get("phone_number")
        except KeyError as error:
            raise DataValidationError("Invalid Account: missing " + error.args[0])
        except TypeError:
            raise DataValidationError(
                "Invalid Account: body of request contained bad or no data"
            )
        return self

    @classmethod
    def all(cls):
        """Returns all of the Accounts in the database"""
        logger.info("Processing all Accounts")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds an Account by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Accounts with the given name"""
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)


class DataValidationError(Exception):
    """Used for data validation errors"""
    pass
