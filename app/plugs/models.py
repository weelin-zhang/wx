#encoding=utf8
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String,Text, ForeignKey, or_,func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
import time

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine('mysql://root:weelin@127.0.0.1/wx?charset=utf8', echo=False)#echo=True日志
Base = declarative_base()#生成orm基类

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(80), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username

class DepartmentType(Base):
    __tablename__ = 'departtypes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    departname = Column(String(32), nullable=False)
    def __repr__(self):
        return '<Type:{}>'.format(self.departname)



class Solution(Base):
    __tablename__ = 'solutions'
    id = Column(Integer, primary_key=True, autoincrement=True)

    troublename = Column(String(100), nullable=False)
    solution = Column(Text(),nullable=False)
    type = relationship('DepartmentType',backref='solutions')
    type_id = Column(Integer,ForeignKey('departtypes.id'))
    def __repr__(self):
        return self.troublename

#Base.metadata.create_all(engine)
Session_class = sessionmaker(bind=engine)##创建与数据库的会话session class
Session = Session_class()#生成Session_class实例


if __name__=='__main__':
    obj = Session.query(Solution).first()
    ob = Session.query(Solution).filter(Solution.type.id==1).first()
    print ob.id
    print obj
    #print dir(Session)
    try:
        print 'begin'
        objs = Session.query(Solution).filter(Solution.troublename.like('%{}%'.format('烦'))).order_by(Solution.id).all()
    except Exception as e:
	print 'error:',e
    if not objs:print 'None'
    #print objs[0].id 

