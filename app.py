import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_babel import Babel

# Configure logging for better debugging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
babel = Babel()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///neomitra.db"
)
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configure Babel for internationalization
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "hi", "ta", "te", "bn", "mr"]

# Initialize extensions with the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# Import routes after app initialization to avoid circular imports
with app.app_context():
    # Import models and routes
    import models  # noqa: F401
    import routes  # noqa: F401
    from routes import get_locale  # noqa: F401
    
    # Initialize Babel after routes to avoid circular imports
    babel.init_app(app, locale_selector=get_locale)

    # Create database tables
    db.create_all()
    
    # Insert sample data
    from routes import insert_sample_data
    insert_sample_data()
