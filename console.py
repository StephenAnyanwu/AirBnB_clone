#!/usr/bin/python3

"""In this module defines a HBNBCommand class"""


import cmd


class HBNBCommand(cmd.Cmd):
    """Impliment a command line interpreter"""
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command (Ctrl-D) to exit the program"""
        return True

    def emptyline(self):
        """Do nothing if nothing is passed"""
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
