
import logging,requests,markdown2,os
from udi_interface import Node,LOGGER,Custom,LOG_HANDLER
from node_funcs import get_valid_node_name
from nodes import Maker1,POST_STATUS

class Controller(Node):

    def __init__(self, poly, primary, address, name):
        super(Controller, self).__init__(poly, primary, address, name)
        self.ready   = False
        self.first_run = True
        self.hb = 0
        self.handler_typed_data_st = None
        self.Notices         = Custom(self.poly, 'notices')
        self.Params          = Custom(self.poly, 'customparams')
        LOGGER.debug(f'params={self.Params}')
        self.poly.subscribe(self.poly.START,                  self.handler_start, address) 
        self.poly.subscribe(self.poly.POLL,                   self.handler_poll)
        self.poly.subscribe(self.poly.LOGLEVEL,               self.handler_log_level)
        self.poly.subscribe(self.poly.CONFIGDONE,             self.handler_config_done)
        self.poly.subscribe(self.poly.CUSTOMPARAMS,           self.handler_params)
        self.poly.subscribe(self.poly.CUSTOMTYPEDDATA,        self.handler_typed_data)

        self.TypedData       = Custom(self.poly, 'customtypeddata')
        self.TypedParams     = Custom(self.poly, 'customtypedparams')
        self.TypedParams.load(
            [
                {
                    'name': 'maker_events',
                    'title': 'IFTTT Maker Event',
                    'desc': 'IFTTT Maker Events',
                    'isList': True,
                    'params': [
                        {
                            'name': 'node_address',
                            'title': 'Node Address',
                            'desc': 'Must be 8 Characters or less, and never change'
                        },
                        {
                            'name': 'node_name',
                            'title': 'Node Name',
                            'desc': 'Must be 8 Characters or less, and never change'
                        },
                        {
                            'name': 'on_event',
                            'title': 'On Event Name',
                            'isRequired': False,
                        },
                        {
                            'name': 'off_event',
                            'title': 'Off Event Name',
                            'isRequired': False,
                        },
                    ]
                },
            ],
            True
        )
        self.poly.ready()
        self.Notices.clear()
        self.session = requests.Session()
        self.poly.addNode(self, conn_status='ST')

    def handler_start(self):
        LOGGER.info(f"Started IFTTT Maker NodeServer {self.poly.serverdata['version']}")
        self.update_profile()
        self.heartbeat()
        #self.check_params()
        configurationHelp = './CONFIGURATION.md'
        if os.path.isfile(configurationHelp):
            cfgdoc = markdown2.markdown_path(configurationHelp)
            self.poly.setCustomParamsDoc(cfgdoc)
        self.ready = True
        LOGGER.info(f'exit {self.name}')

    # For things we only do have the configuration is loaded...
    def handler_config_done(self):
        LOGGER.debug(f'enter')
        self.poly.addLogLevel('DEBUG_MODULES',9,'Debug + Modules')
        LOGGER.debug(f'exit')

    def handler_poll(self, polltype):
        pass

    def query(self):
        self.setDriver('ST', 1)
        self.reportDrivers()

    def heartbeat(self):
        LOGGER.debug('hb={self.hb}')
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def handler_log_level(self,level):
        LOGGER.info(f'enter: level={level}')
        if level['level'] < 10:
            LOGGER.info("Setting basic config to DEBUG...")
            LOG_HANDLER.set_basic_config(True,logging.DEBUG)
        else:
            LOGGER.info("Setting basic config to WARNING...")
            LOG_HANDLER.set_basic_config(True,logging.WARNING)
        LOGGER.info(f'exit: level={level}')

    '''
    Read the user entered custom parameters.  Here is where the user will
    configure the number of child nodes that they want created.
    '''
    def handler_params(self, params):
        LOGGER.debug(f'loading params: {params}')
        self.Params.load(params)
        LOGGER.debug(f'params={self.Params}')

        self.params_valid = False

        if not "API Key" in params:
            self.api_key = ""
            self.Params['API Key'] = self.api_key
            # Must exist because adding the key calls this method again...
            return
        self.api_key = params['API Key']

        if self.api_key == "":
            self.poly.Notices['API Key'] = "Please add your IFTT Key https://ifttt.com/maker_webhooks/settings"
        else:
            # Assume it's good
            self.params_valid = True

    def handler_typed_data(self, typed_data):
        LOGGER.debug("Enter config={}".format(typed_data))
        self.TypedData.load(typed_data)
        self.maker_events = self.TypedData['maker_events']
        #if self.handler_typed_data_st = True:
        # Not the first run, create any new events
        self.add_maker_events()
        self.handler_type_data_st = True

    def add_maker_events(self):
        LOGGER.debug('enter')
        if len(self.maker_events) == 0:
            LOGGER.warning("No Maker Events defined in configuration")
        else:
            for event in self.maker_events:
                if 'node_name' in event:
                    LOGGER.info(f"Adding node for {event}")
                    self.add_maker_node(event)
                else:
                    LOGGER.warning(f"No Event Name in {self.maker_events[i]}")
        LOGGER.debug('exit')

    def add_maker_node(self,event):
        return self.poly.addNode(Maker1(self,self.address,event))

    def delete(self):
        LOGGER.info('Oh No I\'m being deleted. Nooooooooooooooooooooooooooooooooooooooooo.')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def check_params(self):
        pass

    def post(self,event_name,value1=None,value2=None,value3=None):
        LOGGER.debug(f'event_name={event_name} value1={value1} value2={value2} value3={value3}')
        url = f'https://maker.ifttt.com/trigger/{event_name}/with/key/{self.api_key}/'
        #url = f'https://maker.ifttt.com/trigger/bad_event_name/with/key/bad_api_key/'
        #payload = {'value1': value1, 'value2': value2, 'value3': value3}
        payload = {}
        LOGGER.info(f"Sending: {url} payload={payload}")
        try:
            response = self.session.post(url,payload)
        # This is supposed to catch all request excpetions.
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Connection error for {url}: {e}")
            return {'st': False, 'post_status': POST_STATUS['Connection']}

        LOGGER.info(f' Got: code={response.status_code}')
        if response.status_code == 200:
            LOGGER.info(f"Got: text={response.text}")
            return { 'st:': True, 'post_status': POST_STATUS['Success'], 'data':response.text }
        elif response.status_code == 400:
            LOGGER.error(f"Bad request: {url}")
            return { 'st': False, 'post_status': POST_STATUS['Request Error'] }
        elif response.status_code == 404:
            LOGGER.error(f"Not Found: {url}")
            return { 'st': False, 'post_status': POST_STATUS['Invalid Error'] }
        elif response.status_code == 401:
            # Authentication error
            LOGGER.error("Failed to authenticate, please your API Key")
            return { 'st': False, 'post_status': POST_STATUS['Authentication Error'] } 
        else:
            LOGGER.error(f"Unknown response {response.status_code}: {url} {response.text}")
            return { 'st': False, 'post_status': POST_STATUS['Unknow Error'] }

    def update_profile(self):
        LOGGER.info('start')
        st = self.poly.updateProfile()
        return st

    id = 'IFTTTCntl'
    commands = {
      'QUERY': query,
    }
    drivers = [
        {'driver': 'ST',  'value':  1, 'uom':  25} ,
    ]
