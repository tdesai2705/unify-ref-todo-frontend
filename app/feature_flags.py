from rox.server.rox_server import Rox
from rox.server.flags.rox_flag import RoxFlag
from rox.server.rox_options import RoxOptions, NetworkConfigurationsOptions

class _Flags:
    def __init__(self):
        self.due_date_feature = RoxFlag(False)
        self.dark_mode = RoxFlag(False)

flags = _Flags()
_setup_done = False

def setup(api_key):
    global _setup_done
    if _setup_done or not api_key:
        return
    Rox.register(flags)
    # Point SDK to CloudBees FM platform endpoints (not legacy rollout.io)
    options = RoxOptions(network_configuration_options=NetworkConfigurationsOptions(
        get_config_api_endpoint='https://api.cloudbees.io/device/get_configuration',
        get_config_cloud_endpoint='https://rox-conf.cloudbees.io',
        send_state_api_endpoint='https://api.cloudbees.io/device/update_state_store',
        send_state_cloud_endpoint='https://rox-state.cloudbees.io',
        analytics_endpoint='https://api.cloudbees.io/events/flag-impressions',
        push_notification_endpoint='https://api.cloudbees.io/sse',
    ))
    Rox.setup(api_key, options).result()
    _setup_done = True
