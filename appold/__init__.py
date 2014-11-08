from flask import Flask
# from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.admin.contrib.sqla import ModelView
# from flask.ext.admin import Admin, BaseView, expose
# from flask.ext.script import Manager
# from flask.ext.migrate import Migrate, MigrateCommand
import datetime
# class MyView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('index.html')

app = Flask(__name__)

app.config.from_object('config')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/app'
db = SQLAlchemy(app)
from app import views, models

# class HackedSQLAlchemy(SQLAlchemy):
#     def apply_driver_hacks(self, app, info, options):
#         print "Applying driver hacks"
#         super(HackedSQLAlchemy, self).apply_driver_hacks(app, info, options)
#         options["supports_unicode_binds"] = False
# db = HackedSQLAlchemy(app)
# db = SQLAlchemy(app)


# @app.template_filter('reverse')
# def reverse_filter(s):
#     if s > datetime.date.today():
#       return 0
#     else:
#        return 1



# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Bootstrap(app)
# from flask.ext.mail import Mail
# mail = Mail(app)

# admin = Admin(app)
# admin.add_view(ModelView(models.Projects, db.session))
# admin.add_view(ModelView(models.Goals, db.session))
# admin.add_view(ModelView(models.Strategies, db.session))
# admin.add_view(ModelView(models.Tasks, db.session))