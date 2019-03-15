import os
import logging
import rq
import uuid

from elasticsearch import Elasticsearch
from logging.handlers import RotatingFileHandler
from redis import Redis

from config import Config
from flask import Flask, request, current_app
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
login = LoginManager()
login.login_view = 'auth.login' # points to the login view
babel = Babel()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app,db)
	login.init_app(app)
	mail.init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	babel.init_app(app)

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	from app.errors import bp as errors_bp
	app.register_blueprint(errors_bp)

	from app.post import bp as post_bp
	app.register_blueprint(post_bp, url_prefix='/post')

	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')

	from app.admin import bp as admin_bp
	app.register_blueprint(admin_bp, url_prefix='/admin')

	app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
		if app.config['ELASTICSEARCH_URL'] else None

	app.redis = Redis.from_url(app.config['REDIS_URL'])
	app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

	if not app.debug:
		if not os.path.exists('logs'):
			os.mkdir('logs')
		file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
		file_handler.setFormatter(logging.Formatter( '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)
		app.logger.setLevel(logging.INFO)
		app.logger.info('Microblog startup')

	return app

@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(current_app.config['LANGUAGES'])
	#return 'es'

from app import models
