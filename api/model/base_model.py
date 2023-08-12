#!/usr/bin/python3
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(150))
    email = Column(String(200))
    birthdate = Column(String(100))
    jobs = relationship("Jobs", back_populates='users', cascade='all, delete-orphan')
    
    def __repr__(self):
        return "({}) -> {} {}".format(self.id, self.first_name, self.last_name)

class Jobs(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    job_type = Column(String(50))
    location = Column(String(100))
    level = Column(String(100))
    vacancies = Column(Integer)
    salary = Column(Integer)
    deadline = Column(String(50))
    description = Column(String(1000))
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship("User", back_populates="jobs")

    def __repr__(self):
        return "{} - {} -> {}".format(self.id, self.user_id, self.title)
