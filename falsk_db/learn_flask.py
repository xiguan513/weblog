#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///learn_falsk.db'#生产文件到当前目录
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)#新版本修改的地方
db=SQLAlchemy(app)



"""
创建一个User用户表
三个字段id,username,email其中id自动设置为自增长主键id

引用方法

from yourapp import db
hello.py 中引用

"""

class User(db.Model):
    __tablename__='User'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True)
    email=db.Column(db.String(120),unique=True)

    def __init__(self,username,email):
        self.username=username
        self.email=email

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
