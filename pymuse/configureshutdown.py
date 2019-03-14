import sys
from signal import signal, SIGINT, SIGTERM

registered_modules = []

def _signal_handler(sig, frame):
    global registered_modules
    for module in registered_modules:
        module.shutdown()
    sys.exit(0)

def configure_shutdown(*modules):
    """Shutdown every given thread before leaving the main thread when SIGINT or SIGTERM is received"""
    global registered_modules
    registered_modules = list(modules)
    signal(SIGINT, _signal_handler)
    signal(SIGTERM, _signal_handler)
