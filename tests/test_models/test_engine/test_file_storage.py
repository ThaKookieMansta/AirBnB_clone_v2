#!/usr/bin/python3
"""File storage tests"""
import json
import os
from models.base_model import BaseModel
from models.state import State
from models.amenity import Amenity
import unittest
import pep8
from models.place import Place
from models.user import User
from models.review import Review
from models.engine.file_storage import FileStorage
from models.city import City


class TestFilestorage(unittest.TestCase):
    """Test for file storage"""

    @classmethod
    def setUpClass(cls):
        """this method raises an exception while the test is running, the framework will
        consider the test to have suffered an error,
        and the test method will not be executed.
        """
        cls.user = User()
        cls.user.first_name = "Mara"
        cls.user.last_name = "Moja"
        cls.user.email = "maramoja@gmail.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """method that tidies up after the test method has been run"""
        del cls.user

    def tearDown(self):
        """method that tidies up after the test method has been run"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_FileStorage(self):
        """Pep8 test"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_all(self):
        """Checks if everything in file storage works"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_new(self):
        """this method tests new instances"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 345678
        user.name = "Mara"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_filestorage(self):
        """
        This method checks whether the file reloads
        """
        self.storage.save()
        _root = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(_root, "file.json")
        with open(path, 'r') as f:
            lines = f.readlines()
        try:
            os.remove(path)
        except Exception:
            pass
        self.storage.save()
        with open(path, 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except Exception:
            pass
        with open(path, "w") as f:
            f.write("{}")
        with open(path, "r") as r:
            for line in r:
                self.assertEqual(line, "{}")
        self.assertIs(self.storage.reload(), None)


if __name__ == "__main__":
    unittest.main()

