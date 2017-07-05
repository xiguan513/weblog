#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import sys
sys.path.append('./')
sys.path.append('../')
from app import app,db
from app.models import search_log

def search(name):
    project_list = db.session.query(search_log.project_name).all()
    ip=db.session.query(search_log.ip).filter(search_log.project_name=="{}".format(name)).first()[0]
    group=db.session.query(search_log.group).filter(search_log.project_name=="{}".format(name)).first()[0]
    port=db.session.query(search_log.port).filter(search_log.project_name=="{}".format(name)).first()[0]
    log_file=db.session.query(search_log.log_address).filter(search_log.project_name=="{}".format(name)).first()[0]
    return {"ip":ip,"group":group,"port":port,"log_file":log_file,"project_list":project_list}


#指定主机需要用的IP用户名密码端口号等信息
def host(ip):
    info_dict={ip:{"ansible_host":ip,"ansible_port":22,"ansible_user":"root"}}
    print json.dumps(info_dict[ip],indent=4)
#指定组信息
def group():
    info_dict={"all":ip}
    print json.dumps(info_dict,indent=4)

if len(sys.argv) == 2 and (sys.argv[1] == '--list'):
    ip=[]
    for name in search("b2b")["project_list"]:
        name=name[0]
        ip.append(search(name)["ip"])
    group()
elif len(sys.argv) == 3 and (sys.argv[1] == '--host'):
    ip=sys.argv[2]
    host(ip)
else:
    print "Usage: %s --list or --host <hostname>" % sys.argv[0]
    sys.exit(1)





