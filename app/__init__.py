from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

from config import basedir



app = Flask(__name__)
app.config.from_object('config')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
db = SQLAlchemy(app)



from app import views , models