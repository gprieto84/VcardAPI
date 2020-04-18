from flask import Flask
from config import Config
import logging
from logging.handlers import TimedRotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

handler = TimedRotatingFileHandler('logs/app.log', when="D", interval=1)
handler.suffix = "%Y-%m-%d.log"
logging.basicConfig(level=logging.DEBUG,\
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s', handlers=[handler])

app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models