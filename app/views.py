from flask import render_template, request, Response
import datetime
from app import app,db
from .models import ms_mi_log, total_log,search_log
import time
import os
import re
import sys
import commands



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
    return render_template("greplog.html",project_grep=project_list)

# @app.route('/admin')
# def admin():
#     return render_template("admin.html")


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


def outlog(ip,First_time,Last_time):
    ip=str(ip)
    logfile=search_log.query.filter_by(project_name='{}'.format(ip)).first()
    first_time_list = First_time.split(' ')[0]
    common = """ansible {hostname} -m script -a "/home/song/tomcat_log_time.sh '{First}' '{Last}' {logfile}" """
    (status,output) = commands.getstatusoutput(common.format(hostname=ip,First=First_time, Last=Last_time, logfile=logfile))

    if status==0:
        log_name=time.strftime('%Y-%m-%d-%H-%M')+".log"
        with open(log_name,"w") as f:
            f.write(output)
        yield "Down log file %s" % log_name
    else:
        yield "Get Log File Fail! start: %s endtime:%s" % (First_time,Last_time)


@app.route('/query')
def query():
    ip=request.args.get("project")
    First_time = request.args.get("First Time").replace('T', ' ')
    Last_time = request.args.get("Last Time").replace('T', ' ')
    return Response(outlog(ip,First_time, Last_time),
                    mimetype="text/event-stream")


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


def event_stream(ip,filter=None):
    logfile=search_log.query.filter_by(project_name='{}'.format(ip)).first()
    command = '''ansible {hostname} -a "tail -n10 {logfile}"'''
    textlist = os.popen(command.format(hostname=ip,logfile=logfile)).readlines()
    for line in textlist:
        if filter is not None:
            re_filter=re.compile(r'(%s)'%filter,re.I)
            if re.findall(re_filter,line):
                res=re.sub(re_filter,r'<font color="red">\1</font>',line)
                yield 'data: %s\n\n' % res.rstrip()
        else:
            yield 'data: %s\n\n' % line.rstrip()



@app.route('/stream/<ip>')
@app.route('/stream/<ip>/<filter>')
def stream(ip, filter=None):
    return Response(event_stream(ip, filter),
                    mimetype="text/event-stream")





def event_keywords(ip,filter):
    ip = str(ip)
    logfile = search_log.query.filter_by(project_name='{}'.format(ip)).first()
    command = '''ansible {hostname} -a "grep -n {filter} {logfile}"'''
    textlist = os.popen(command.format(hostname=ip,filter=filter,logfile=logfile)).readlines()
    for line in textlist:
        if filter is not None:
            re_filter=re.compile(r'(%s)'%filter,re.I)
            if re.findall(re_filter,line):
                res=re.sub(re_filter,r'<font color="red">\1</font>',line)
                yield 'data: %s\n\n' % res.rstrip()
        else:
            yield 'data: %s\n\n' % "Query condition is empty. Please confirm"


@app.route('/greplog/<ip>/<filter>')
def keywords(ip, filter,):
    return Response(event_keywords(ip,filter),
                    mimetype="text/event-stream")