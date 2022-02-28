#
# IFTTT Webhooks Base Node
#
#
from udi_interface import Node,LOGGER
from node_funcs import get_valid_node_address,get_valid_node_name

class Base(Node):

    def __init__(self, controller, primary, event):
        self.controller = controller
        self.event = event
        self.ready = False
        if not 'node_address' in event:
            LOGGER.error(f"No node_address in {event}")
        if event['node_address'] == "":
            LOGGER.error(f"node_address is null {event}")
        address = get_valid_node_address(event['node_address'])
        if not 'node_name' in event:
            LOGGER.error(f"No node_name in {event}")
        if event['node_name'] == "":
            LOGGER.error(f"node_name is null {event}")
        if 'on_event' in event and event['on_event'] != "":
            self.on_event = event['on_event']
            self.id += "On"
        else:
            self.on_event = None
        if 'off_event' in event and event['off_event'] != "":
            self.off_event = event['off_event']
            self.id += "Off"
        else:
            self.off_event = None
        name    = get_valid_node_name(event['node_name'])
        self.pfx = f"{name}:"
        LOGGER.debug(f'{self.pfx} controller={controller} event={event}')
        super().__init__(controller.poly, primary, address, name)
        controller.poly.subscribe(controller.poly.START,  self.handler_start, address) 

    def handler_start(self):
        LOGGER.info(f'{self.pfx} enter')
        self.ready = True
        LOGGER.info(f'{self.pfx} exit')

    def query(self):
        LOGGER.info(f'{self.pfx} enter')
        self.reportDrivers()
        LOGGER.info(f'{self.pfx} exit')

    def post(self,event):
        ret = self.controller.post(event)
        LOGGER.debug("Got: {ret}")
        self.setDriver('ST',ret['post_status'])

    def cmd_set_on(self, command):
        if self.on_event is None:
            LOGGER.error("On Event is not defined")
            return
        self.post(self.on_event)

    def cmd_set_off(self, command):
        if self.off_event is None:
            LOGGER.error("Off Event is not defined")
            return
        self.post(self.off_event)


