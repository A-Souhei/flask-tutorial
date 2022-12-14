from flask import Flask
from config import Config # Important to import the config file

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config) # Important to load the config

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from app import routes, models

# run:  flask db init
# run: flask db migrate
# run: flask db upgrade
# run: flask db migrate -m "posts table"
# run: flask db upgrade