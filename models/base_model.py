#!/usr/bin/python3
"""
This module carries the base model for the entire AIRBNB Project
"""
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()


class BaseModel:
    """
    This is the base class for the entire AirBnb project
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        This method initializes the instance with the specific
        variables that are specified
        """

        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """
            This method returns the printable output for the class
            :return:
            """
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """
        This method updates the current time to the updated_at attribute
        :return:
        """

        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        models.storage.save()

    def to_dict(self):
        """
        :return: Returns a dictionary containing all keys/values
        of __dict__ of the instance.
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop("_sa_instance_state", None)
        return my_dict

    def delete(self):
        """
        Deletes the current instance from storage
        Returns:

        """
        models.storage.delete(self)
