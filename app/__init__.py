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

from flask_moment import Moment


from flask_babel import Babel

from flask import request


app = Flask(__name__)
app.config.from_object(Config)  # Important to load the config

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

mail = Mail(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

babel = Babel(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app import routes, models

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


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])   # Important to set the language
    return 'fr'

# run : module 'jinja2.ext' has no attribute 'autoescape'
# then run : pybabel init -i messages.pot -d app/translations -l fr
# then run: pybabel compile -d app/translations

# to update
# run: pybabel extract -F babel.cfg -k _l -o messages.pot .
# run: pybabel update -i messages.pot -d app/translations
