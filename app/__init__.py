from flask import Flask
from config import Config # Important to import the config file

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config) # Important to load the config

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# run:  flask db init