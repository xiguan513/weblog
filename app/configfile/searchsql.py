#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
sys.path.append('../../')
from app import app,db
from app.models import search_log

def search(name):
    project_list = db.session.query(search_log.project_name).all()
    ip=db.session.query(search_log.ip).filter(search_log.project_name=="{}".format(name)).first()[0]
    group=db.session.query(search_log.group).filter(search_log.project_name=="{}".format(name)).first()[0]
    port=db.session.query(search_log.port).filter(search_log.project_name=="{}".format(name)).first()[0]
    log_file=db.session.query(search_log.log_address).filter(search_log.project_name=="{}".format(name)).first()[0]
    return {"ip":ip,"group":group,"port":port,"log_file":log_file,"project_list":project_list}


if __name__=="__main__":
    for name in search("b2c")["project_list"]:
        ip=search(name[0])["ip"]
        print ip