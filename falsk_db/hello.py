#!/usr/bin/env python
#-*- coding: utf-8 -*-


#创建数据库
from learn_flask import db
#db.create_all()


#创建用户
from learn_flask import User
#admin=User('admin',"admin@admin.com")
#guest=User('guest','guest@admin.com')



#插入数据,并提交
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()

#查询表数据
userall=User.query.all()
print userall

#条件查询
admin = User.query.filter_by(username='administraotr').first()

#打印原始sql
print str(User.query.filter_by(username='administraotr'))

#把数据查出来以后重新修改数据
# admin.username="administraotr"
# admin.email="admimistrator@admin.com"
# db.session.add(admin)
# db.session.commit()