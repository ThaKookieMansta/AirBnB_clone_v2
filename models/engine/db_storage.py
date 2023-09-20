#!/usr/bin/python3
"""
Defines the DBStorage Engine for the project
"""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker



class DBStorage:
    """
    This Class represents the dbstorage engine
    """
    __engine = None
    __session = None

    def __int__(self):
        """
        Initializes the DBStorage instances
        """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on current db session
        Args:
            cls:

        Returns: Dictionary file

        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """
        Adds the object to the current db session
        Args:
            obj:

        Returns:

        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes to the current db session
        Returns:

        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current db session
        Args:
            obj:

        Returns:

        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the db
        Returns:

        """
        Base.metadata.create_all(self.__engine)
        curr_db_session = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        safe_session = scoped_session(curr_db_session)
        self.__session = safe_session()

    def close(self):
        """
        Closes all working SQLAclhemy sessions
        Returns:

        """
        self.__session.close()
