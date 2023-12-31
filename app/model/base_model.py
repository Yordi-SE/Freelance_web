from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from model import storage
from flask_login import UserMixin

Base = declarative_base()

from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return storage.query(int(user_id))

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(150))
    email = Column(String(200), unique=True)
    birthdate = Column(String(100))
    password = Column(String(300))
    filename = Column(String(200))
    jobs = relationship("Jobs", back_populates='users', cascade='all, delete-orphan')
    
    def __repr__(self):
        return "({}) -> {} {}".format(self.email, self.first_name, self.last_name)

class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String(400))
    title = Column(String(200))
    job_type = Column(String(100))
    location = Column(String(100))
    level = Column(String(100))
    vacancies = Column(Integer)
    salary = Column(String(400))
    deadline = Column(String(50))
    description = Column(String(1000))
    user_email = Column(String(200), ForeignKey('users.email', onupdate='CASCADE'), nullable=False)
    users = relationship("User", back_populates="jobs")

    def __repr__(self):
        return "{} - {} -> {}".format(self.id, self.user_email, self.title)

class Applied(Base):
    __tablename__ = 'applied'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_email = Column(String(200), nullable=False)
    job_id = Column(Integer, nullable=False)
