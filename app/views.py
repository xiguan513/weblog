from flask import render_template, request, Response
import datetime
from app import app, db
from .models import ms_mi_log, total_log
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
    return render_template("hosts.html")


@app.route('/weblog')
def weblog():
    return render_template("weblog.html")


@app.route('/greplog')
def greplog():
    return render_template("greplog.html")

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


def outlog(First_time,Last_time):
    logfile="/alidata/www/logs/catalina-2017-06-22.log"
    first_time_list = First_time.split(' ')[0]
    common = """ansible test -m script -a "/home/song/tomcat_log_time.sh '{First}' '{Last}' {logfile}" """
    (status,output) = commands.getstatusoutput(common.format(First=First_time, Last=Last_time, logfile=logfile))

    if status==0:
        for line in output.readlines():
            yield '%s\n\n' % line
    else:
        yield "Get Log File Fail!"


@app.route('/query')
def query():
    First_time = request.args.get("First Time").replace('T', ' ')
    Last_time = request.args.get("Last Time").replace('T', ' ')
    return Response(outlog(First_time, Last_time),
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


def event_stream(logfile,filter=None):
    logfile="/alidata/www/logs/%s" % logfile
    command = '''ansible test -a "tail -n10 %s"''' % (logfile)
    textlist = os.popen(command).readlines()
    for line in textlist:
        if filter is not None:
            re_filter=re.compile(r'(%s)'%filter,re.I)
            if re.findall(re_filter,line):
                res=re.sub(re_filter,r'<font color="red">\1</font>',line)
                yield 'data: %s\n\n' % res.rstrip()
        else:
            yield 'data: %s\n\n' % line.rstrip()



@app.route('/stream/<logfile>')
@app.route('/stream/<logfile>/<filter>')
def stream(logfile, filter=None):
    return Response(event_stream(logfile, filter),
                    mimetype="text/event-stream")




def event_keywords(logfile,filter):
    logfile="/alidata/www/logs/%s" % logfile
    command = '''ansible test -a "grep -n %s %s"''' % (filter,logfile)
    textlist = os.popen(command).readlines()
    for line in textlist:
        if filter is not None:
            re_filter=re.compile(r'(%s)'%filter,re.I)
            if re.findall(re_filter,line):
                res=re.sub(re_filter,r'<font color="red">\1</font>',line)
                yield 'data: %s\n\n' % res.rstrip()
        else:
            yield 'data: %s\n\n' % "Query condition is empty. Please confirm"


@app.route('/greplog/<logfile>/<filter>')
def keywords(logfile, filter,):
    return Response(event_keywords(logfile, filter),
                    mimetype="text/event-stream")