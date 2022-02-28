#
# Webhook IFTTT Node
#

from udi_interface import LOGGER
from nodes import Base

class Webhook(Base):

    def __init__(self, controller, primary, event):
        # May have different id's in the future?
        self.id = 'Webhook'
        # For now we just call the Base super
        super().__init__(controller, primary, event)

    def cmd_set_on(self,command):
        super().cmd_set_on(command)

    def cmd_set_off(self,command):
        super().cmd_set_off(command)

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 25},
    ]
    commands = {
        'DON': cmd_set_on,
    }
