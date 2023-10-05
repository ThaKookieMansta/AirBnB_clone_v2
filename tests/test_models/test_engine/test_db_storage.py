#!/usr/bin/python3
"""File storage tests"""
import unittest
import pep8
import json
import os
from os import getenv
import MySQLdb
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
class TestDBStorage(unittest.TestCase):
    """db_storage file test"""


    @classmethod
    def setUpClass(cls):
        """this method raises an exception while the test is running, the framework will
        consider the test to have suffered an error,
        and the test method will not be executed.
        """
        cls.User = getenv("HBNB_MYSQL_USER")
        cls.Passwd = getenv("HBNB_MYSQL_PWD")
        cls.Db = getenv("HBNB_MYSQL_DB")
        cls.Host = getenv("HBNB_MYSQL_HOST")
        cls.db = MySQLdb.connect(host=cls.Host, user=cls.User,
                                 passwd=cls.Passwd, db=cls.Db,
                                 charset="utf8")
        cls.query = cls.db.cursor()
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def teardown(cls):
        """method that tidies up after the test method has been run"""
        cls.query.close()
        cls.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_db_storage(self):
        """Pep8 Test"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_all_tables(self):
        """this method tests tables"""
        self.query.execute("SHOW TABLES")
        output = self.query.fetchall()
        self.assertEqual(len(output), 7)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_user_elements(self):
        """this method tests elements"""
        self.query.execute("SELECT * FROM users")
        output = self.query.fetchall()
        self.assertEqual(len(output), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_cities_elements(self):
        """this method tests elements"""
        self.query.execute("SELECT * FROM cities")
        output = self.query.fetchall()
        self.assertEqual(len(output), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'NO DB')
    def test_add(self):
        """this method adds two nums and checks if the result is equal to expected
         sum.
         """
        self.query.execute("SELECT * FROM states")
        output = self.query.fetchall()
        self.assertEqual(len(output), 0)
        state = State(name="LUISILLO")
        state.save()
        self.db.autocommit(True)
        self.query.execute("SELECT * FROM states")
        output = self.query.fetchall()
        self.assertEqual(len(output), 1)


if __name__ == "__main__":
    unittest.main()
