from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField, DateField,TextAreaField,SelectMultipleField,IntegerField
from wtforms import validators
from wtforms import widgets


class project_form(Form):
    project = TextField('Project *', [validators.Required(),validators.Length(min=2, max=50)] ) 
    projectleader = TextField('Project Leader *(required)', [validators.Required(),validators.Length(min=4, max=35,message='not the right length')] ) 
    submit=SubmitField('Add Project')

class goal_form(Form):
    goal = TextAreaField('Goal', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
    submit=SubmitField('Add Objective')

class strategy_form(Form):
    strategy = TextAreaField('Strategy', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
    submit=SubmitField('Add Strategy')

class task_form(Form):
    task = TextAreaField('Task', [validators.Required(),validators.Length(min=2, max=200,message='not the right length')])
    staff = TextField('Staff Assigned')
    complete = BooleanField('Is the task Complete?')
    deadline =DateField( 'Deadline (mm/dd/yyyy)',  format='%m/%d/%Y',validators = [validators.Required()])
    note = TextAreaField('Note',[validators.Required(),validators.Length(min=2, max=250,message='not the right length less than 250 characters')])
    Order = IntegerField('Order')
    submit=SubmitField('Submit')

class DeleteRow_form(Form):
    row_id = IntegerField('')
    submitd = SubmitField('Delete')
