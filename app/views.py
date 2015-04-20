from app import app
from flask import Flask, render_template, request, flash,redirect,url_for,jsonify
from forms import goal_form, strategy_form, project_form, task_form,DeleteRow_form,ldapA
import models 
import datetime
from sqlalchemy.orm.attributes import get_history
from werkzeug import secure_filename
import re, shutil, os, sys
from sqlalchemy.sql import func
from sqlalchemy import case
from sqlalchemy import and_
from app.models import Tasks, Projects, Goals, Strategies
from app import db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import socket
from threading import Thread


@app.route('/navstart', methods=['GET','POST'])
def navstart():
    aform=ldapA()
    email=None
    AS=None
    if aform.validate_on_submit():
        import sys
        import ldap
        l = ldap.initialize("ldap://10.129.18.101")
        email=None
        try:
            l.simple_bind_s("program\%s" % aform.username.data,aform.password.data)
            print "Authentification Successful"
            r=l.search_s('cn=Users,dc=BHCS,dc=Internal',ldap.SCOPE_SUBTREE,'(sAMAccountName=*%s*)' % aform.username.data,['mail'])
            email=r[0][1]['mail']
            AS=1
            print email
        except:
            print 'Failed'
            AS=0
        print email
        # return render_template("navStart.html",aform=aform,email=email,AS=AS)
    return render_template("navStart.html",aform=aform,email=email,AS=AS)


@app.route('/sendemail', methods=['GET', 'POST'])
def sendEmailV4():
    # subject = ''
    recipient=', '.join(['cmeinzer@acbhcs.org'])
    body='html text'
    subject = 'subjectline'
    headers = ["From: " + 'chet@acbhcs.org',
               "Subject: " + 'subject',
               "To: " + 'cmeinzer@acbhcs.org',
               "MIME-Version: 1.0",
               "Content-Type: text/html"]
    headers = "\r\n".join(headers)
    session = smtplib.SMTP("allsmtp.acgov.org",25)
    session.ehlo()
    session.starttls()
    session.ehlo
    session.sendmail('chet@acbhcs.org', ['cmeinzer@acbhcs.org'], headers + "\r\n\r\n" + body)
    session.quit()
    return "it worked"

app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    pform=project_form()
    tform=task_form()
    sform=strategy_form()
    gform=goal_form()
    P=models.Projects.query.all()
    if gform.validate_on_submit():
        u=models.Projects.query.get(1)
        p=models.Goals(goal=gform.goal.data,proj=u)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("baseindex.html",pform=pform,gform=gform,tform=tform,sform=sform,P=P)

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

@app.route('/start', methods=['GET','POST'])
def start():
    pform=project_form()
    P=models.Projects.query.all()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).outerjoin(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id))  
    if request.method == 'POST':
        if pform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(pform)
            return redirect(url_for('start'))
        else:
            p=models.Projects(name=pform.project.data,projectleader=pform.projectleader.data)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('start'))
    return render_template("index_for_project.html",pform=pform,P=P,zipit=zip(P,q_sum))

@app.route('/ProjectTree/<name>', methods=['GET','POST'])
def project_outline(name):
    # name=request.args.get('name')
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    G=project.goals.all()
    gform=goal_form(request.values)
    delete_form=DeleteRow_form()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    Goals.id.label("goal_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).join(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id,Goals.id).filter(Projects.id == name) )
    if request.method == 'POST' and  gform.submit.data:
        if gform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(gform)
            return redirect(url_for('project_outline', name=name))
        else:
            p=models.Goals(goal=gform.goal.data,proj=project)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('project_outline', name=name))
    if request.method == 'POST' and  delete_form.submitd.data:
        pstratrow = delete_form.row_id.data
        pstrat=models.Goals.query.filter_by(id=pstratrow).first()
        db.session.delete(pstrat)
        db.session.commit()
        return redirect(url_for('project_outline',name=name))            
    # if request.method == 'POST' and  delete_form.submit.data:
    #     delete_row=
    return render_template("index_for_goal.html",project=project,G=G,gform=gform,P=P,zipit=zip(G,q_sum),delete_form=delete_form)

@app.route('/ProjectTree/<name>/<goal>', methods=['GET','POST'])
def strategy_outline(name,goal):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    S=pgoal.strategies.all()
    sform=strategy_form(request.values)
    delete_form=DeleteRow_form()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    Strategies.id.label("strategy_id"),
    Goals.id.label("goal_id"),
    ).join(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id,Goals.id,Strategies.id).filter(Goals.id == goal) )
    if request.method == 'POST' and sform.submit.data:
        print sform.validate()
        if sform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(sform)
            return redirect(url_for('strategy_outline',name=name,goal=goal))
        else:
            p=models.Strategies(strategy=sform.strategy.data,goa=pgoal)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('strategy_outline',name=name,goal=goal))
    if request.method == 'POST' and  delete_form.submitd.data:
        pstratrow = delete_form.row_id.data
        pstrat=models.Strategies.query.filter_by(id=pstratrow).first()
        db.session.delete(pstrat)
        db.session.commit()
        return redirect(url_for('strategy_outline',name=name,goal=goal))
    return render_template("index_for_strategy.html",project=project,S=S,sform=sform,pgoal=pgoal,P=P,zipit=zip(S,q_sum),delete_form=delete_form)

@app.route('/strategysort/<goal>')
def strategy_sort(goal):
    P=models.Projects.query.all()
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    S=pgoal.strategies.all()
    project=models.Projects.query.filter_by(id=pgoal.project_id).first()
    return render_template("sort_strategy.html",q_sum=S,project=project,goal=pgoal,P=P)

@app.route('/order/<table>')
def order(table):
    sortedItems = request.args.listvalues()[0]
    o=1
    table = getattr(models, table)
    for item in sortedItems:
        grab = table.query.filter_by(id=item).first() 
        grab.order=o
        o+=1
    db.session.commit()
    return jsonify(result="New Order Saved!")

@app.route('/tasksort/<strategy>')
def task_sort(strategy):
    P=models.Projects.query.all()
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    T=pstrat.tasks.all()
    goal=models.Goals.query.filter_by(id=pstrat.goal_id).first()
    project=models.Projects.query.filter_by(id=goal.project_id).first()
    return render_template("sort_task.html",q_sum=T,project=project,goal=goal,strategy=strategy,P=P)

@app.route('/ProjectTree/<name>/<goal>/<strategy>', methods=['GET','POST'])
def task_outline(name,goal,strategy):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    # T=(pstrat.tasks.order_by(pstrat.tasks.Order)).all()
    T=pstrat.tasks.all()
    tform=task_form(request.values)
    if request.method == 'POST':
        if tform.validate() == False:
            flash('Failed Field validation.')
            flash_errors(tform)
            return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
        else:
            if tform.complete.data == True:
                completeDate=datetime.datetime.utcnow()
                print completeDate
                p=models.Tasks(task=tform.task.data,strat=pstrat,note = tform.note.data,staff=tform.staff.data,deadline=tform.deadline.data,complete=tform.complete.data,created=datetime.datetime.utcnow(), completeDate=completeDate)
            else:
                p=models.Tasks(task=tform.task.data,strat=pstrat,note = tform.note.data,staff=tform.staff.data,deadline=tform.deadline.data,complete=tform.complete.data,created=datetime.datetime.utcnow())
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template("index_for_task.html",project=project,T=T,tform=tform,pstrat=pstrat,pgoal=pgoal,P=P)

@app.route('/outlineindex')
def outline_index():
    P=models.Projects.query.all()
    return render_template("index_for_outline.html",P=P)

@app.route('/outline/<name>' )
def outline(name):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    return render_template("index_outline_all.html",P=P,project=project)

@app.route('/edit/<name>/<goal>/<strategy>/<task>', methods=['GET', 'POST'])
def edit_task(name,goal,strategy,task):
    P=models.Projects.query.all()
    project=models.Projects.query.filter_by(id=name).first() 
    pgoal=models.Goals.query.filter_by(id=goal).first() 
    pstrat=models.Strategies.query.filter_by(id=strategy).first() 
    ptask=models.Tasks.query.filter_by(id=task).first()
    delete_form=DeleteRow_form()
    form = task_form(obj=ptask)
    form.populate_obj(ptask)
    form.deadline.data = ptask.deadline.strftime("%m/%d/%Y")
    tform=task_form(request.values)
    if request.method == 'POST' and form.validate_on_submit():
        #if it changed from True to false, set complete date to None
        # import pdb;pdb.set_trace()
        if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[False]:
            print 'changed from false to true'
            ptask.completeDate=datetime.datetime.utcnow()
        if get_history(ptask, 'complete')[0]==[False] and get_history(ptask, 'complete')[2]==[True]:
            print 'changed from true to false'
            ptask.completeDate=None
        else:
            if get_history(ptask, 'complete')[0]==[True] and get_history(ptask, 'complete')[2]==[None]:
                ptask.complete=True
                ptask.completeDate=None
        db.session.commit()
        return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    if delete_form.validate_on_submit():
        db.session.delete(ptask)
        db.session.commit()
        return redirect(url_for('task_outline',name=name,goal=goal,strategy=strategy))
    return render_template('edit_task.html', tform=tform,form=form,project=project,pgoal=pgoal,pstrat=pstrat,ptask=ptask,delete_form=delete_form,P=P)


@app.route('/graphs')
def graphs():
    P=models.Projects.query.all()
    return render_template("index_for_graphs.html", P=P)

@app.route('/graphs/stats')
def graphs_stats():
    P=models.Projects.query.all()
    q_sum = (db.session.query(
    Projects.id.label("project_id"),
    func.sum(case([(Tasks.complete == True, 1)], else_=0)).label("x"),
    func.sum(case([(and_(Tasks.deadline != None, Tasks.completeDate != None, Tasks.deadline > Tasks.completeDate), 1)], else_=0)).label("y"),
    func.count(Tasks.id).label("total"),
    ).outerjoin(Goals, Projects.goals).outerjoin(Strategies, Goals.strategies).outerjoin(Tasks, Strategies.tasks).group_by(Projects.id))   
    return render_template("graph_stats.html", P=P,q_sum=q_sum,zipit=zip(P,q_sum))



from app import db
