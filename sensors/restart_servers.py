from st2reactor.sensor.base import PollingSensor
import json
from st2client.client import Client
from st2client.models import KeyValuePair

class RestartServersSensor(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            - get_logger() - returns logger instance specific to this sensor.
            - dispatch() for dispatching triggers into the system.
    * self._config
        - contains parsed configuration that was specified as
          config.yaml in the pack.
    """

    def __init__(self, sensor_service, config, poll_interval=20):
        super(RestartServersSensor, self).__init__(
            sensor_service = sensor_service,
            config = config,
            poll_interval = poll_interval
        )
        self.logger = None
        self.client = None

    def setup(self):
        # Setup stuff goes here. For example, you might establish connections
        # to external system once and reuse it. This is called only once by the system.
        self.logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self.client = Client(base_url='http://localhost')

    def poll(self):
        key_name = self._config.get('server_config_key_name', { "entries": []})
        servers_json = self.client.keys.get_by_name(name=key_name)
        if servers_json:
          self.logger.debug('servers: ' + servers_json)
          servers_object = json.loads(servers_json.value)
          trigger = "mock_portal.server_stopped"
          for server_id, server in servers_object.items():
            if server.get("server_state") == "stopped":
              self.logger.debug('found stopped server: ' + server_id)
              self._sensor_service.dispatch(trigger=trigger, payload={
                  "server_id": server_id
              })

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform cleanup operations like
        # closing the connections to external system here.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass