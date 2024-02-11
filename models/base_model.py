#!/usr/bin/python3

"""In this module defines the BaseModel class"""

import uuid
from datetime import datetime
import re


class BaseModel:
    """
    Impliment the base class for all models

    Attributes
    ----------
    id : str (instance attribute)
        The unique identifier of a created user
    created_at : datetime.datetime (instance attribute)
        The date and time a new user is created.
    updated_at : datetime.datetime (instance attribute)
        The date and time a user (profile) is updated.

    Methods
    -------
    save()
         Update the public instance attribute updated_at with the
         current datetime
    to_dict()
        Return a dictionary containing all keys/values of __dict__
        of the instance
    __str__()
         Return and print the string representation of BaseModel object
    """
    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        *args : any type (optional, non-keyworded arguments)
        **kwargs : any type (optional, keyworded arguments)
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs and len(kwargs) > 0:
            for key, value in kwargs.items():
                time_fmt = '%Y-%m-%d %H:%M:%S.%f'
                if key == "created_at":
                    # replace the 'T' in str type  datetime with ' '
                    value_fmt = re.sub('T', ' ', value)
                    # convert the str type datetime to datetime object
                    self.created_at = datetime.strptime(value_fmt, time_fmt)
                elif key == "updated_at":
                    # replace the 'T' in str type  datetime with ' '
                    value_fmt = re.sub('T', ' ', value)
                    # convert the str type datetime to datetime object
                    self.updated_at = datetime.strptime(value_fmt, time_fmt)

    def save(self):
        """
        Update the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Return a dictionary containing all keys/values of
        __dict__ of the instance.
        The created_at and updated_at keys in the dictionary
        are of string type datetime
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        return obj_dict

    def __str__(self):
        """
        Return and print the string representation of BaseModel object
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
