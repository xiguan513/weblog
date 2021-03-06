#-*- coding:utf-8 -*-
from flask import render_template, request, Response
import datetime
from app import app,db
from .models import ms_mi_log, total_log,search_log
import time
import os
import re
import sys
import commands
import json
from app.configfile import searchsql


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hosts')
def hosts():
    project_list = db.session.query(search_log.project_name).all()
    return render_template("hosts.html",project_list=project_list)


@app.route('/weblog')
def weblog():
    project_list = db.session.query(search_log.project_name).all()
    return render_template("weblog.html",project_real=project_list)


@app.route('/greplog')
def greplog():
    project_list = db.session.query(search_log.project_name).all()
    return render_template("greplog.html", project_grep=project_list)


#@app.route('/down')
def downlog():
    return render_template("downfile.html")

@app.route('/index')
def main():
    interval_date = datetime.datetime.now() - datetime.timedelta(days=7)
    interval_date_str = interval_date.strftime('%Y-%m-%d')

    ms_data = total_log.query.filter(total_log.date > interval_date_str).filter_by(app_name='ms').order_by('date')
    mi_data = total_log.query.filter(total_log.date > interval_date_str).filter_by(app_name='mi').order_by('date')
    echarts_date = ','.join(["'%s'" % i.date for i in ms_data])

    ms_data_str = ','.join([str(i.total) for i in ms_data])
    mi_data_str = ','.join([str(i.total) for i in mi_data])
    return render_template("ms_mi.html", echarts_date=echarts_date, ms_data_str=ms_data_str, mi_data_str=mi_data_str)




@app.route('/api', methods=['POST'])
def api():
    ip = request.remote_addr
    rc = request.form.get('rc', None)
    uin = request.form.get('uin', None)
    mbox = request.form.get('mbox', None)
    des = request.form.get('des', None)
    print ip, rc, uin, mbox, des
    log_err = ms_mi_log(ip=ip, rc=rc, uin=uin, mbox=mbox, des=des)
    db.session.add(log_err)
    db.session.commit()
    return 'OK'

#实时日志加关键字
def event_stream(ip,filter=None):
    print ip
    #logfile=db.session.query(search_log.log_address).filter(search_log.project_name=="{}".format(ip)).first()[0]
    #logfile=search_log.query.filter_by(project_name='{}'.format(ip)).first()
    logfile=searchsql.search(ip)["log_file"]
    command = '''ansible -i app/configfile/hosts.py {hostname} -a "tail -n10 {logfile}"'''
    print command
    ip = searchsql.search(ip)["ip"]
    textlist = os.popen(command.format(hostname=ip,logfile=logfile))
    for line in textlist.readlines():
        if  filter!=None:
            re_filter=re.compile(r'(%s)'%filter,re.I)
            if re.findall(re_filter,line):
                res=re.sub(re_filter,r'<font color="red">{}</font>'.format(filter),line)
                yield 'data: %s\n\n' % res.rstrip()
            else:
                yield 'data: %s\n\n' % line.rstrip()
        else:
            yield 'data: %s\n\n' % line.rstrip()


@app.route('/stream/<ip>')
@app.route('/stream/<ip>/<filter>')
def stream(ip, filter=None):
    return Response(event_stream(ip, filter),
                    mimetype="text/event-stream")






#关键字查询
def event_keywords(ip,filter):
    data = {
        u'status': u'ok',
        u'message': u'success',
        u'datas': [

        ]
    }
    ip = str(ip)
    line_num=500
    logfile = searchsql.search(ip)["log_file"]
    print logfile
    command = '''ansible -i app/configfile/hosts.py {hostname} -a "grep -n {filter} {logfile}"'''
    print command
    ip=searchsql.search(ip)["ip"]
    (status, output) = commands.getstatusoutput(command.format(hostname=ip,filter=filter,logfile=logfile))
    #print commands.getstatusoutput(command.format(hostname=ip,filter=filter,logfile=logfile))
    if status==0:
        output=output.split("\n")
        with open("app/static/data/page.json","w") as grepoutput:
            for i in output:
                a = {"dataNum": i}
                data[u"datas"].append(a)
            grepoutput.write(json.dumps(data))
        return render_template("greplog.html")
    else:
        return '%s\n\n' % "Query condition is empty. Please confirm"





@app.route('/grep')
def keywords():
    ip = request.args.get("project")
    filter = request.args.get("filter")
    return Response(event_keywords(ip,filter))



#根据时间
def outlog(ip,First_time,Last_time):
    ip=str(ip)
    logfile = searchsql.search(ip)["log_file"]
    print logfile
    common = """ansible -i app/configfile/hosts.py {hostname} -m script -a "/home/song/tomcat_log_time.sh '{First}' '{Last}' {logfile}" """
    print common.format(hostname=ip,First=First_time, Last=Last_time, logfile=logfile)
    ip = searchsql.search(ip)["ip"]
    (status,output) = commands.getstatusoutput(common.format(hostname=ip,First=First_time, Last=Last_time, logfile=logfile))
    if status==0:
        log_dir="/home/song/weblog/logs/"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_name=time.strftime('%Y-%m-%d-%H-%M')+".log"
        with open(log_dir+log_name,"w") as f:
            f.write(output)
        return render_template("downfile.html",log_name=log_name)


    else:
        return "Get Log File Fail! start: %s endtime:%s" % (First_time,Last_time)


@app.route('/query')
def query():
    ip=request.args.get("project")
    First_time = request.args.get("First Time").replace('T', ' ')
    Last_time = request.args.get("Last Time").replace('T', ' ')
    return Response(outlog(ip,First_time, Last_time),
                    mimetype="text/event-stream,text/html")