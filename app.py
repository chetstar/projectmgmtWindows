#!flask/bin/python
from app import app

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager, UserMixin, login_required



# class HackedSQLAlchemy(SQLAlchemy):
#     def apply_driver_hacks(self, app, info, options):
#         print "Applying driver hacks"
#         super(HackedSQLAlchemy, self).apply_driver_hacks(app, info, options)
#         options["supports_unicode_binds"] = False
# db = HackedSQLAlchemy(app)

import os
basedir = os.path.abspath(os.path.dirname(__file__))


# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# from sqlalchemy import create_engine
# SQLALCHEMY_DATABASE_URI = create_engine("mssql+pyodbc://dashboarddatadev", encoding='windows-1255', convert_unicode=True)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)
# import pdb;pdb.set_trace()


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()