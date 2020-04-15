from api import db, ma
from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

assignees_for_tasks = db.Table('assignees_for_tasks',
    db.Column('assignee_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'))
    )

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
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
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    planned_complete_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    comments = db.relationship('Comment', backref='task', lazy='dynamic')
    assignees = db.relationship('User',
        secondary=assignees_for_tasks,
        backref=db.backref('tasks', lazy='dynamic'),
        lazy='dynamic'
        )

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return Task.query.all()

    def add_assignee(self, assignee):
        self.assignees.append(assignee)
        db.session.add(self)

    def remove_assignee(self, assignee):
        self.assignees.remove(assignee)
        db.session.add(self)

    def update_completed_state(self, old_task_completed):
        print("Self completed")
        print(self.completed)
        print("OG task completed")
        print(old_task_completed)
        if self.completed != old_task_completed:
            print("Got to first if")
            if self.completed:
                print("Got to second if")
                self.completed_at = datetime.utcnow()
            else:
                self.completed_at = None
        return self

    def __repr__(self):
        return f'<Task {self.name} | Created at {self.created_at} | {self.completed} | Completed at {self.completed_at}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return User.query.all()

    def __repr__(self):
        return f'<User {self.name}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        Comment.query.all()

    def __repr__(self):
        return f'<Comment {self.content} | Created at {self.created_at} | Updated at {self.updated_at}>'

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------
class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        include_fk = True
        load_instance = True
        sqla_session = db.session


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        sqla_session = db.session

class TaskSchema(SQLAlchemyAutoSchema):
    comments = Nested(CommentSchema, many=True)
    assignees = Nested(UserSchema, many=True)
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

