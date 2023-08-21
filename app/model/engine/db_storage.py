#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    __session = None
    __engine = None
    def __init__(self):
        self.__engine = create_engine('mysql+pymysql://Yordi:Yordi@localhost/my_free')

    def new(self, obj):
        self.__session.add(obj)

    def all(self, cls):
        obj = self.__session.query(cls).all()
        return obj

    def job(self):
        from model.base_model import Jobs, User
        obj = self.__session.query(Jobs).filter(Jobs.user_email == User.email)
        return obj

    def save(self):
        self.__session.commit()

    def reload(self):
        from model.base_model import Base
        Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def delete(self, obj):
        if obj is not None:
            self.__session.delete(obj)
    
    def query(self, field):
        from model.base_model import User
        obj = self.__session.query(User).filter(User.id == field).first()
        return obj
    
    def query_email(self, field):
        from model.base_model import User
        obj = self.__session.query(User).filter(User.email == field).first()
        return obj
    def close(self):
        self.__session.close()
    
    def query_job(self, field):
        from model.base_model import Jobs
        obj = self.__session.query(Jobs).filter(Jobs.id == field).first()
        return obj
    
    def query_job_title(self, field):
        from model.base_model import Jobs
        obj = self.__session.query(Jobs).filter(Jobs.title == field).all()
        return obj
    
    def query_email_job(self, field):
        from model.base_model import Jobs
        obj = self.__session.query(Jobs).filter(Jobs.user_email == field)
        return obj
    
    def query_page(self, page, lim):
        from model.base_model import Jobs
        off = (page - 1) * lim
        obj = self.__session.query(Jobs).order_by(Jobs.id.desc()).offset(off).limit(lim).all()
        return obj
    
    def query_page_email(self, field, page, lim):
        from model.base_model import Jobs
        off = (page - 1) * lim
        obj = self.__session.query(Jobs).filter(Jobs.user_email == field).offset(off).limit(lim).all()
        return obj