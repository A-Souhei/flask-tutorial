from flask import Flask
from config import Config  # Important to import the config file

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_login import LoginManager

import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

from flask_mail import Mail

from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)  # Important to load the config

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

mail = Mail(app)

bootstrap = Bootstrap(app)

from app import routes, models, errors

# run:  flask db init
# run: flask db migrate
# run: flask db upgrade
# run: flask db migrate -m "posts table"
# run: flask db upgrade

# run:  flask db migrate -m "new fields in user model"
# run: flask db upgrade

login.login_view = 'login'

# second terminal then run: python -m smtpd -n -c DebuggingServer localhost:8025 | alternative is sendgrid
# could have done this in SEIE ???
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        # write logs into file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

