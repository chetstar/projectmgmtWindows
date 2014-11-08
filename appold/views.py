from flask import render_template
from app import app
import models
from app import db


@app.route('/')
@app.route('/index')
def index():
    x=models.User.query.all()
    user = {'nickname': 'Chet'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'someone'}, 
            'body': 'Beautiful day in Portland!' 
        },

    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts,
                           x=x)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#               (form.openid.data, str(form.remember_me.data)))
#         return redirect('/index')
#     return render_template('login.html', 
#                            title='Sign In',
#                            form=form)