# Home Assistant Event Monitor

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
<br><a href="https://www.buymeacoffee.com/Petro31" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-black.png" width="150px" height="35px" alt="Buy Me A Coffee" style="height: 35px !important;width: 150px !important;" ></a>

_Event Monitor app for AppDaemon._

Displays specified events inside the appdaemon logs.

## Installation

Download the `event_monitor` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `hacs` module.

## Example App configuration

#### Basic
```yaml
# Monitors all events in INFO log level
events:
  module: event_monitor
  class: EventMonitor
  level: 'INFO'
```

#### Advanced
```yaml
# Monitors all switch call_services
events:
  module: event_monitor
  class: EventMonitor
  level: 'INFO'
  events:
  - event: call_service
    data:
      domain: 'switch'
```

#### App Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | events | The module name of the app.
`class` | False | string | IlluminateDoor | The name of the Class.
`level` | True | `'INFO'` &#124; `'DEBUG'` | `'DEBUG'` | Switches log level.
`events` | False | list | | A list of event names or event objects.

#### Event Object Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`event` | False | string | | The entity_id of the switch or light.
`data` | True | map | | Basic event data.  Currently does not accept sublists or sub dictionaries.
