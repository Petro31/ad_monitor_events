import appdaemon.plugins.hass.hassapi as hass
import voluptuous as vol

CONF_MODULE = 'module'
CONF_CLASS = 'class'
CONF_EVENTS = 'events'
CONF_LEVEL = 'level'
CONF_EVENT = 'event'
CONF_DATA = 'data'

LOG_ERROR = 'ERROR'
LOG_DEBUG = 'DEBUG'
LOG_INFO = 'INFO'

EVENT_SCHEMA = [ vol.Any(
        str,
        { 
            vol.Required(CONF_EVENT): str,
            vol.Optional(CONF_DATA): {str: vol.Any(int, str, bool)},
        })]

APP_SCHEMA = vol.Schema({
    vol.Required(CONF_MODULE): str,
    vol.Required(CONF_CLASS): str,
    vol.Optional(CONF_EVENTS, default=[]): EVENT_SCHEMA,
    vol.Optional(CONF_LEVEL, default=LOG_INFO): vol.Any(LOG_INFO, LOG_DEBUG),
})

class EventMonitor(hass.Hass):
    def initialize(self):
        args = APP_SCHEMA(self.args)

        # Set Lazy Logging (to not have to restart appdaemon)
        self._level = args.get(CONF_LEVEL)

        self.events = events = [ AppEvent(e) for e in args.get(CONF_EVENTS) ]

        self.handles = []

        if events:
            for event in events:
                self.log(f"Monitoring {event.tostring()}", level=self._level)
                
                if event.data:
                    handle = self.listen_event(self.monitor_event, event.event, **event.data)
                else:
                    handle = self.listen_event(self.monitor_event, event.event)
                self.handles.append(handle)
        else:
            self.log("Monitoring all events", level=self._level)
            self.handles.append(self.listen_event(self.monitor_event))

    def monitor_event(self, event_name, data, kwargs):
        self.log(f"{event_name}: {data}", level=self._level)

    def terminate(self):
        for i, handle in enumerate(self.handles):
            self.log(f"Canceling handle {i}", level=self._level)
            self.cancel_listen_event(handle)
            
class AppEvent(object):
    def __init__(self, evt):
        self.data = {}
        if isinstance(evt, dict):
            self.event = evt.get(CONF_EVENT)
            self.data = evt.get(CONF_DATA, {})
        elif isinstance(evt, str):
            self.event = evt

    def tostring(self):
        if self.data:
            return f"{{'event':'{self.event}', 'data':{self.data}}}"
        else:
            return f"{{'event':'{self.event}'}}"
