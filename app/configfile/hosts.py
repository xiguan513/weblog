#!/usr/bin/python
#-*- coding:utf-8 -*-

import json
import sys
sys.path.append('../')
sys.path.append('../../')
from searchsql import search

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





