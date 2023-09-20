#!/usr/bin/python3
"""
This module contains the class File storage which handles
serialization and deserialization of the dictionaries
"""
import json
import datetime

from models.base_model import BaseModel


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
        obj_dict = obj.to_dict()
        key = f"{obj_dict['__class__']}.{str(obj.id)}"
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        Returns:
        """
        new_dict = self.__objects
        object_dictionary = {obj_id: obj.to_dict() for obj_id, obj in
                             new_dict.items()}

        for obj_id in object_dictionary:
            obj_data = object_dictionary[obj_id]
            for key, value in obj_data.items():
                if isinstance(value, datetime.datetime):
                    obj_data[key] = value.strftime(BaseModel.DATE_FORMAT)

        with open(FileStorage.__file_path, mode="w") as json_file:
            json.dump(object_dictionary, json_file)


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
        with open(FileStorage.__file_path) as json_file:
            reloaded_dict = json.load(json_file)
            for obj_data in reloaded_dict.values():
                if "__class__" in obj_data:
                    class_name = obj_data.pop("__class__")
                    cls = globals().get(class_name)
                    if cls and issubclass(cls, BaseModel):
                        obj = cls(**obj_data)
                        self.new(obj)
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
