from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler
from flask_mail import Mail
from flask_cors import CORS  # Import CORS here
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
scheduler = APScheduler()
mail = Mail()
cors = CORS()  # Initialize CORS here
