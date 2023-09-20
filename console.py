#!/usr/bin/python3
"""
This program contains the entry point of the command intepreter
"""
import cmd
import sys
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """
    This class contains the functionality for the console
    """

    intro = "Welcome to the HBNB console"
    prompt = "(hbnb) "

    hbnb_cmd_list = [
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    ]

    def do_quit(self, command):
        """
        Exits the interactive shell
        Args:
            command:

        Returns:

        """
        exit()


    def do_EOF(self, arg):
        """
        Exits the interactive shell
        Args:
            arg:

        Returns:

        """
        print()
        exit()


    def emptyline(self):
        """
        This method executes nothing when there is an
        empty line
        Returns:

        """
        pass

    def do_create(self, arg):
        """
        This method creates a new instance of
        Base Model, saves it to a json file and
        prints the id
        Args:
            arg: The class name

        Examples:
            create BaseModel

        Returns:

        """
        try:
            if not arg:
                raise SyntaxError()
            args_list = arg.split(" ")

            kwargs = {}
            for i in range(1, len(args_list)):
                key, value = tuple(args_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(args_list[0])()
            else:
                obj = eval(args_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        This method prints the string representation of an instance
        based on the class name and  id
        Args:
            arg

        Examples:
            show <class Name> <id>
            show BaseModel 1234-1234-1234

        Returns:

        """
        try:
            if not arg:
                raise SyntaxError()
            my_list = arg.split(" ")
            if my_list[0] not in self.hbnb_cmd_list:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")


    def do_destroy(self, args):
        """
        This method deletes an instance based on the class name
        ,and it's ID
        Args:
            args

        Examples:
            destroy <class name> <id>
            destroy BaseModel 1234-1234-1234

        Returns:

        """
        try:
            if not args:
                raise SyntaxError()
            my_list = args.split(" ")
            if my_list[0] not in self.hbnb_cmd_list:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")


    def do_all(self, args):
        """
        This method prints all string representation of all
        instances either alone or by class name
        Args:
            args: The class name

        Examples:
            all BaseModel
            all

        Returns:

        """
        if not args:
            o = storage.all()
            print([o[k].__str__() for k in o])
            return
        try:
            args = args.split(" ")
            if args[0] not in self.hbnb_cmd_list:
                raise NameError()

            o = storage.all(eval(args[0]))
            print([o[k].__str__() for k in o])

        except NameError:
            print("** class doesn't exist **")

    def do_count(self, args):
        """
        This method counts the number of instances of a class
        Args:
            args:

        Example:
            count UserUser f650f143-6b7a-4630-a21b-562cda8f4a04
            {'first_name': 'Chris', 'age': '32'}
        Returns:

        """
        counter = 0
        try:
            my_list = split(args, " ")
            if my_list[0] not in self.hbnb_cmd_list:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == my_list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def do_update(self, args):
        """
        This method updates an instance based on the class name and
        id by adding or updating attributes
        Args:
            args:

        Examples:
            update <class name> <id> <attribute> "<value>"
            update BaseModel 1234-1234-1234 email "aibnb@mail.com"

        Returns:

        """
        try:
            if not args:
                raise SyntaxError()
            my_list = split(args, " ")
            if my_list[0] not in self.__classes:
                raise NameError()
            if len(my_list) < 2:
                raise IndexError()
            objects = storage.all()
            key = my_list[0] + '.' + my_list[1]
            if key not in objects:
                raise KeyError()
            if len(my_list) < 3:
                raise AttributeError()
            if len(my_list) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[my_list[2]] = eval(my_list[3])
            except Exception:
                v.__dict__[my_list[2]] = my_list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")



if __name__ == "__main__":
    HBNBCommand().cmdloop()
