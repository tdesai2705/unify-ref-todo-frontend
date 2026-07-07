from rox.server.rox_server import Rox
from rox.server.flags.rox_flag import RoxFlag
from rox.server.rox_options import RoxOptions

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
    Rox.setup(api_key, RoxOptions()).result()
    _setup_done = True
