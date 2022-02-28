
""" Node classes used by the IFTTT Webhooks Node Server. """

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
from .Webhook    import Webhook
from .Controller import Controller
