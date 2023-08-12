#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage:
    __session = None
    __engine = None
    def __init__(self):
        self.__engine = create_engine('mysql://root:root@localhost/my_free')

    def new(self, obj):
        self.__session.add(obj)

    def all(self, cls):
        obj = self.__session.query(cls).all()
        return obj

    def job(self):
        from model.base_model import Jobs, User
        obj = self.__session.query(Jobs).filter(Jobs.user_id == User.id)
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

