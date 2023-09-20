#!/usr/bin/python3
"""test for city"""
import unittest
import os
from os import getenv
from models.city import City
from models.base_model import BaseModel
import pep8


class TestCity(unittest.TestCase):
    """class Test City"""

    @classmethod
    def setUpClass(cls):
        """this method raises an exception while the test is running, the framework will
        consider the test to have suffered an error,
        and the test method will not be executed.
        """
        cls.city = City()
        cls.city.name = "NBI"
        cls.city.state_id = "NKR"

    @classmethod
    def teardown(cls):
        """method that tidies up after the test method has been run"""
        del cls.city

    def tearDown(self):
        """method that tidies up after the test method has been run"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_City(self):
        """Pep8 test"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/city.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_City(self):
        """this method checks the documentation"""
        self.assertIsNotNone(City.__doc__)

    def test_attributes_City(self):
        """checks the attributes of the city"""
        self.assertTrue('id' in self.city.__dict__)
        self.assertTrue('created_at' in self.city.__dict__)
        self.assertTrue('updated_at' in self.city.__dict__)
        self.assertTrue('state_id' in self.city.__dict__)
        self.assertTrue('name' in self.city.__dict__)

    def test_is_subclass_City(self):
        """checks whether City is a subclass of Basemodel"""
        self.assertTrue(issubclass(self.city.__class__, BaseModel), True)

    def test_attribute_types_City(self):
        """this method checks the attribute type of the city"""
        self.assertEqual(type(self.city.name), str)
        self.assertEqual(type(self.city.state_id), str)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == 'db', 'DB')
    def test_save_City(self):
        """checks whether save works"""
        self.city.save()
        self.assertNotEqual(self.city.created_at, self.city.updated_at)

    def test_to_dict_City(self):
        """this method checks whether dictionary works"""
        self.assertEqual('to_dict' in dir(self.city), True)


if __name__ == "__main__":
    unittest.main()

