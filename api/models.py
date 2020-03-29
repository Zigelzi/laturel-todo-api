from api import db, ma
from datetime import datetime

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

    @staticmethod
    def get_all():
        return Project.query.all()

    def __repr__(self):
        return f'<Project {self.name} | {self.description} | created {self.created_at} | {self.completed} | completed {self.completed_at}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)
    planned_complete_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    

    def save(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @staticmethod
    def get_all():
        return Task.query.all()

    def __repr__(self):
        return f'<Task {self.title} | created {self.created_at} | {self.completed} | completed {self.completed_at}>'

# ---------------------------------
# Marshmallow serialization schemas
# ---------------------------------

class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project