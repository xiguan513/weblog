#!/usr/bin/env python
#-*- coding:utf-8 -*-


from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db

db.except_all('tail_log')

