"""
Service Package
"""
import os

from flask import Flask
from flask_cors import CORS
from flask_talisman import Talisman

# Create the Flask app
app = Flask(__name__)

# Configure the database (SQLite by default)
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///development.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# This must be imported after the Flask app is created
from service import routes  # pylint: disable=wrong-import-position,cyclic-import
from service.common import error_handlers  # noqa: F401 pylint: disable=wrong-import-position
from service.common import log_handlers  # pylint: disable=wrong-import-position
from service.models import init_db  # pylint: disable=wrong-import-position,cyclic-import

log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Initialize the database
init_db(app)

# Add CORS support and security headers
CORS(app)
Talisman(
    app,
    force_https=False,
    content_security_policy={"default-src": ["'self'"], "object-src": ["'none'"]},
)
