from app import db,login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def __repr__(self):
        return '<User %r>' % self.username

class DepartmentType(db.Model):
    __tablename__ = 'departtypes'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departname = db.Column(db.String(32), nullable=False)
    def __repr__(self):
        return '<Type:{}>'.format(self.departname)


class Solution(db.Model):
    __tablename__ = 'solutions'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    troublename = db.Column(db.String(100), nullable=False)
    solution = db.Column(db.Text(),nullable=False)
    type = db.relationship('DepartmentType',backref='solutions')
    type_id = db.Column(db.Integer,db.ForeignKey('departtypes.id'))
    def __repr__(self):
        return self.troublename

@login_manager.user_loader
def load_user(user_id):
    user=User.query.get(int(user_id))
    return user



if __name__=='__main__':
    db.create_all()
