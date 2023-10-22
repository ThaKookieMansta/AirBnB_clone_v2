#!/usr/bin/python3
"""
This module contains the class File storage which handles
serialization and deserialization of the dictionaries
"""
import json
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
        if cls:
            same_type = dict()

            for key, obj in self.__objects.items():
                if obj.__class__ == cls:
                    same_type[key] = obj

            return same_type

        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        Args:
            obj:

        Returns:
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        Returns:
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON
        file (__file_path) exists ; otherwise, do nothing.
        If the file doesn't exist, no exception should be raised)

        Returns:

        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it inside
        Args:
            obj: Object to be deleted if condition is met

        Returns:

        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)

            if self.__objects[key]:
                del self.__objects[key]
                self.save()

    def close(self):
        """Call the reload method."""
        self.reload()
