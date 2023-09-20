#!/usr/bin/python3
"""test for state"""
import unittest
import os
from models.state import State
from models.base_model import BaseModel
import pep8


class TestState(unittest.TestCase):
    """this will test the State class"""

    @classmethod
    def setUpClass(cls):
        """this method raises an exception while the test is running, the framework will
        consider the test to have suffered an error,
        and the test method will not be executed.
        """
        cls.state = State()
        cls.state.name = "CA"

    @classmethod
    def teardown(cls):
        """method that tidies up after the test method has been run"""
        del cls.state

    def tearDown(self):
        """method that tidies up after the test method has been run"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_Review(self):
        """Pep8 test"""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/state.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_checking_for_docstring_State(self):
        """this method checks the documentation"""
        self.assertIsNotNone(State.__doc__)

    def test_attributes_State(self):
        """this method checks whether State has attributes"""
        self.assertTrue('id' in self.state.__dict__)
        self.assertTrue('created_at' in self.state.__dict__)
        self.assertTrue('updated_at' in self.state.__dict__)
        self.assertTrue('name' in self.state.__dict__)

    def test_is_subclass_State(self):
        """this method checks whether State is a subclass of BaseModel"""
        self.assertTrue(issubclass(self.state.__class__, BaseModel), True)

    def test_attribute_types_State(self):
        """this method checks the attribute type of State"""
        self.assertEqual(type(self.state.name), str)

    def test_save_State(self):
        """this method checks whether save works"""
        self.state.save()
        self.assertNotEqual(self.state.created_at, self.state.updated_at)

    def test_to_dict_State(self):
        """this method checks whether dictionary works"""
        self.assertEqual('to_dict' in dir(self.state), True)


if __name__ == "__main__":
    unittest.main()
