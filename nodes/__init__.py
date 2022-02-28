
""" Node classes used by the IFTTT Maker Node Server. """

import udi_interface

POST_STATUS = {
    "None": 0,
    "Success": 1,
    "Network Error": 2,
    "Request Error": 3,
    "Invalid Error": 4,
    "Authentication Error": 5,
    "Data Error": 6,
    "Other Error": 10,
}
from .Base       import Base
from .Maker1     import Maker1
from .Controller import Controller
