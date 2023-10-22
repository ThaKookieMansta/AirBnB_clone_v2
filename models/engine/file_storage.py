#!/usr/bin/python3
"""
This module contains the class File storage which handles
serialization and deserialization of the dictionaries
"""
import json


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
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        Returns:
        """
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON
        file (__file_path) exists ; otherwise, do nothing.
        If the file doesn't exist, no exception should be raised)

        Returns:

        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
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
        """Call the reload method."""
        self.reload()