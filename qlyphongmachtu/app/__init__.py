from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)

app.secret_key = '@#$%^&#@$%^$%^&*@#$%^&43567*#$%^&*'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/qlpmt_db?charset=utf8mb4' % quote('Nhatcuong123@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)