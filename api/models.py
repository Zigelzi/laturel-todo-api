from api import db, ma
from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    planned_complete_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    tasks = db.relationship('Task', backref='project', lazy='dynamic')

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    def has_tasks(self):
        has_tasks = False
        tasks = self.tasks.all()
        if tasks != []:
            has_tasks = True
        return has_tasks

    @staticmethod
    def get_all():
        return Project.query.all()

    def __repr__(self):
        return f'<Project {self.name} | {self.description} | created {self.created_at} | {self.completed} | completed {self.completed_at}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    planned_complete_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return Task.query.all()

    def __repr__(self):
        return f'<Task {self.name} | Created at {self.created_at} | {self.completed} | Completed at {self.completed_at}>'

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_fk = True
        load_instance = True
        sqla_session = db.session

class ProjectSchema(SQLAlchemyAutoSchema):
    tasks = Nested(TaskSchema, many=True)
    class Meta:
        model = Project
        load_instance = True
        sqla_session = db.session