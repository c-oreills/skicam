from datetime import datetime, timedelta
import subprocess
from time import sleep

from eventlet import spawn_after

from utils import shutdown_server

TIMEOUT = timedelta(minutes=3)

def _cache():
    from skiweb import cache
    return cache

def reset_timeout():
    _cache().set('last_event', datetime.now())

def disable_timeout():
    _cache().set('timeout_enabled', False)

def init_timeout():
    reset_timeout()
    _cache().set('timeout_enabled', True)
    check_timeout()

def check_timeout():
    if not _cache().get('timeout_enabled'):
        return

    last_event = _cache().get('last_event')
    secs_left = (last_event + TIMEOUT - datetime.now()).total_seconds()

    if secs_left > 0:
        spawn_after(secs_left, check_timeout)
        return

    terminate()

def terminate():
    #turn_off_wifi()
    shutdown_server()

def turn_off_wifi():
    subprocess.call(['ifdown', 'wlan0'])

def turn_on_wifi():
    subprocess.call(['ifup', 'wlan0'])
