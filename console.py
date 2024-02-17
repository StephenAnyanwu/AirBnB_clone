#!/usr/bin/python3

"""In this module defines a HBNBCommand class"""


import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import models
import re


class HBNBCommand(cmd.Cmd):
    """Impliment a command line interpreter"""
    prompt = "(hbnb) "
    CLASSES = {"BaseModel": BaseModel,
               "User": User,
               "State": State,
               "City": City,
               "Amenity": Amenity,
               "Place": Place,
               "Review": Review}

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command (Ctrl-D) to exit the program"""
        return True

    def emptyline(self):
        """Do nothing if nothing is passed"""
        pass

    def do_create(self, line):
        """Create a new instance of a class, saves
        it (to the JSON file) and prints the id"""
        # Note: 'line' is the command line arguments
        # in our case a class name.
        if line == "":
            # if no class is passed
            print("** class name missing **")
        elif line not in self.CLASSES:
            # if class passed doesn't exist
            print("** class doesn't exist **")
        else:
            new_obj = self.CLASSES[line]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, line):
        """Prints the string representation of an instance
        base on class name and id"""
        args = line.split()
        if not args:
            # if no class name is passed
            print("** class name missing **")
            return
        elif args[0] not in self.CLASSES:
            # if class name passed doesn't exist
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            # if id is not passed
            print("** instance id missing **")
            return
        else:
            args_concat = args[0] + "." + args[1]
            # if class name and id passed doesn't exist
            if args_concat not in models.storage.all() or len(args):
                print("** no instance found **")
                return
            obj_str = models.storage.all()[args_concat]
            # if class name and id passed exist
            print(obj_str)

    def do_destroy(self, line):
        """Delete an instance base on class name and id"""
        args = line.split()
        if len(args) == 0:
            # if no class name is passed
            print("** class name missing **")
            return
        elif args[0] not in self.classes:
            # if class name passed doesn't exist
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            # if id is not passed
            print("** instance id missing **")
            return
        else:
            args_concat = args[0] + "." + args[1]
            # if class name and id passed don't match
            if args_concat not in models.storage.all() or len(args) < 2:
                print("** no instance found **")
                return
            models.storage.delete(args_concat)

    def do_all(self, line):
        """Print all string representation of all instances based or
        not on the class name in a list format"""
        if not line:
            # if no class name is passed, print all objects
            listed_objs = [str(obj) for obj in models.storage.all().values()]
            print(listed_objs)
            return
        elif line in self.CLASSES:
            # if class name is passed and it exist
            listed_objs = []
            for obj_id, obj in models.storage.all().items():
                class_name = obj_id.split(".")[0]
                if class_name == line:
                    listed_objs.append(str(obj))
            print(listed_objs)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """
        Update an instance based on class name and id by adding or updating
        attribute (save the change into the JSON file.
        Usage: update <class name> <id> <attribute name> '<attribute value>'       
        Rules to follow:
            >> Only “simple” arguments can be updated: string, integer and float.
            >> You can assume arguments are always in the right order.
            >> Each arguments are separated by a space.
            >> A string argument with a space must be between double quote.
            >> The error management starts from the first argument to the last one.
            >> All other argument is not used if number of arguments exceed 4.
            >> id, created_at, updated_at attribute name can't be updated.
        """
        # arguments in a list
        args = line.split()
        forbidden_attr_name = ["id", "created_at", "updated_at"]
        if len(args) == 0:
            # if no class name is passed
            print("** class name missing **")
            return
        elif args[0] not in self.CLASSES:
            # if class name passed doesn't exist
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            # if id is not passed
            print("** instance id missing **")
            return
        elif args[0] + "." + args[1] not in models.storage.all():
            # if class name and id passed doesn't exist
            print("** no instance found **")
            return
        elif len(args) < 3:
            # if attribute name is not passed
            print("** attribute name missing **")
            return
        elif len(args) < 4:
            # if attribute value is not passed
            print("** value missing **")
            return
        else:
            in_quote = False
            # convert the last arguments to space seperated strings
             last_args_concat = " ".join(args[3:])
             # find strings between double quotes and store then in a list
             str_list = re.findall(r'\"([^\"]*)\"', last_args_concat)
             if len(str_list) > 0:
                 # If there are strings between double quotes in str_list
                 # let the first string be the attribute value and
                 # the rest be discarded.
                 # Typecast the attribute value to str
                 args[3] = str(str_list[0])
                 args = args[:4]
                 in_quote = True
            else:
                args = args[:4]
            if in_quote is False:
                # Typecast the fourth argument if it's not in quoates
                try:
                     args[3] = eval(args[3])
               except Exception as e:
                   args[3] = str(args[3])
            if args[2] not in forbidden_attr_name:
                if type(args[3]) == str or type(args[3]) == int or type(args[3]) == float:
                    class_id_concat = args[0] + "." + args[1]
                    obj_name = models.storage.all()[class_id_concat]
                    obj_dict = obj_name.to_dict()
                    obj_dict[args[2]] = args[3]
                    new_obj = self.classes[args[0]](**obj_dict)
                    models.storage.new(new_obj)
                    new_obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
