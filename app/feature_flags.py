from rox.server.rox_server import Rox
from rox.server.flags.rox_flag import RoxFlag

class _Flags:
    def __init__(self):
        # Names must match flags registered in CloudBees FM (underscores, not hyphens)
        # These appear in FM console as due_date_feature and dark_mode after first app run
        self.due_date_feature = RoxFlag(False)
        self.dark_mode = RoxFlag(False)

flags = _Flags()
_setup_done = False

def setup(api_key):
    global _setup_done
    if _setup_done or not api_key:
        return
    Rox.register(flags)
    Rox.setup(api_key).result()
    _setup_done = True
