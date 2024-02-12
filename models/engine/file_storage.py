#!/usr/bin/python3

"""In this module defines FileStorage class"""

import json


class FileStorage:
    """
    Impliment and manipulate storage of objects (users' data) in a file

    Attributes
    ----------
    __file_path : str (private class attribute)
        JSON file where objects (users' data) is stored
    __objects : dict (initialized empty)
        store all objects by <class name>.id (ex: to store a BaseModel
        object with id=12121212, the key will be BaseModel.12121212)

    Methods
    -------
    __classes()
        Import classes from models.base_model module and return a
        dictionary of classes
    all()
        Return the dictionary '__objects'
    new(obj)
        Set in '__objects' the 'obj' with key <obj class name>.id
    save()
        Serialize '__objects' to the JSON file (path: __file_path)
    reload()
        Deserialize the JSON file to '__objects'
        (only if __file_path exists)
    """
    __file_path = "file.json"
    __objects = {}

    def __classes(self):
        """Import classes from models.base_model module and
        return a dictionary of classes
        """
        # importing in this method is done to avoid
        # circular imports error
        from models.base_model import BaseModel
        CLASSES = {"BaseModel": BaseModel}
        return CLASSES

    def all(self):
        """Return the dictionary '__objects' """
        return self.__objects

    def new(self, obj):
        """Set in '__objects' the 'obj' with key <obj class name>.id

            Paramters
            ---------
            obj : any object in models.base_model module (e.g BaseModel)
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serialize '__objects' to the JSON file (path: __file_path)"""
        #  holds new objects (data) to be serialised
        new_objs = {}
        for key, obj_name in self.__objects.items():
            new_objs[key] = obj_name.to_dict()
        try:
            #  if file exist, load its content to a variable
            with open(self.__file_path, 'r') as jf:
                json_to_py = json.load(jf)
            if type(json_to_py) is dict:
                #  modify the loaded file content with new objects
                for key, obj_dict in new_objs.items():
                    if key not in json_to_py:
                        json_to_py[key] = obj_dict
            new_objs = json_to_py
        except Exception as e:
            pass
        finally:
            #  modify the file with new objects (data)
            with open(self.__file_path, 'w') as jf:
                json.dump(new_objs, jf)

    def reload(self):
        """Deserialize the JSON file to '__objects'
        (only if __file_path exists)"""
        try:
            with open(self.__file_path, 'r') as f:
                deserialized_objs = json.load(f)
            for key, obj_dict in deserialized_objs.items():
                obj_name = obj_dict["__class__"]
                self.__objects[key] = self.__classes()[obj_name](**obj_dict)
        except Exception as e:
            pass
