#!/usr/bin/python3
"""This module defines the DBStorage class for HBNB project"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage():
    """This class manages storage of hbnb models in a MySQL database"""
    __engine = None
    __session = None
    classes = {
               'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

    def __init__(self):
        """Initialize DBStorage instance"""
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        db_url = 'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db)
        self.__engine = create_engine(db_url, pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session"""
        dic = {}
        if cls is None:
            data = self.__session.query(State).all()
            data += self.__session.query(City).all()
            data += self.__session.query(User).all()
            data += self.__session.query(Place).all()
            data += self.__session.query(Review).all()
            data += self.__session.query(Amenity).all()
            for inst in data:
                key = inst.__class__.__name__ + '.' + inst.id
                dic[key] = inst
        else:
            for inst in self.__session.query(DBStorage.classes[cls]).all():
                key = inst.__class__.__name__ + '.' + inst.id
                dic[key] = inst
        return dic

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)
        self.__session.commit()

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.close()
