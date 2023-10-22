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
        db_uri = "{0}+{1}://{2}:{3}@{4}:3306/{5}".format(
            'mysql', 'mysqldb', getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'), getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB'))

        self.__engine = create_engine(db_uri, pool_pre_ping=True)
        self.reload()

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query on current db session
        Args:
            cls:

        Returns: Dictionary file

        """
        entities = dict()

        if cls:
            return self.get_data_from_table(cls, entities)

        for entity in all_classes:
            entities = self.get_data_from_table(eval(entity), entities)

        return entities

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
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def get_data_from_table(self, cls, structure):
        """Get the data from a MySQL Table
        """

        if type(structure) is dict:
            query = self.__session.query(cls)

            for _row in query.all():
                key = "{}.{}".format(cls.__name__, _row.id)
                structure[key] = _row

            return structure

    def close(self):
        """
        Closes all working SQLAclhemy sessions
        Returns:

        """
        self.__session.close()
