#-*-coding:utf-8-*-
from flask import Flask
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

from config import basedir



app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'
app.config.from_object('config')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
db = SQLAlchemy(app)

admin = Admin(app,name=u'Admin')

from app import views , models

class MyV1(ModelView):

    column_labels = {
        'id':u'序号',
        'ip':u'IP',
        'project_name' : u'主机名',
        'port': u'端口号',
        'group': u'组名',
        'log_address':u'日志路径'

    }
    column_list = ('id','ip','project_name','port','group','log_address')
    def __init__(self, session, **kwargs):
        super(MyV1, self).__init__(models.search_log,session, **kwargs)


admin.add_view(MyV1(db.session,name=u"主机添加"))

