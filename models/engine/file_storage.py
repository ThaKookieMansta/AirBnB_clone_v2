#!/usr/bin/python3
"""
This module contains the class File storage which handles
serialization and deserialization of the dictionaries
"""
import json
import datetime

from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """
    This class is the file storage class that handles
    serialization and deserialization of the dictionaries
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns: The dictionary Objects
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        Args:
            obj:

        Returns:
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        Returns:
        """
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)


def reload(self):
    """
    deserializes the JSON file to __objects (only if the JSON
    file (__file_path) exists ; otherwise, do nothing.
    If the file doesn't exist, no exception should be raised)

    Args:
        self:

    Returns:
    """
    try:
        with open(self.__file_path, "r", encoding="utf-8") as f:
            for o in json.load(f).values():
                name = o["__class__"]
                del o["__class__"]
                self.new(eval(name)(**o))
    except FileNotFoundError:
        pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it inside
        Args:
            obj: Object to be deleted if condition is met

        Returns:

        """
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """
        Calls the reload method
        Args:
            self:

        Returns:

        """
        self.reload()
