from itertools import chain
import json
from os import kill
import signal


OPTIONS = {
    '--exposure': {
        'auto': 'Use automatic exposure mode',
        'night': 'Select setting for night shooting',
        'nightpreview': '',
        'backlight': 'Select setting for back lit subject',
        'spotlight': '',
        'sports': 'Select setting for sports (fast shutter etc)',
        'snow': 'Select setting optimised for snowy scenery',
        'beach': 'Select setting optimised for beach',
        'verylong': 'Select setting for long exposures',
        'fixedfps': 'Constrain fps to a fixed value',
        'antishake': 'Antishake mode',
        'fireworks': '',
    }
}

CONF_FILES = {
    'pic': '/home/pi/skicam/pic.conf',
    'vid': '/home/pi/skicam/vid.conf'
}

current_confs = {'pic': [], 'vid': []}

parent = None

def set_parent(p):
    global parent
    parent = int(p)


def generate_conf(type, config):
    conf = {}
    for k, v in config.iteritems():
        if v in OPTIONS.get(k, {}):
            conf[k] = v
    return conf

def write_conf(type, conf):
    open(CONF_FILES[type], 'w').write(json.dumps(conf))
    if parent:
        kill(parent, signal.SIGUSR1)

def read_conf(type):
    try:
        return json.loads(open(CONF_FILES[type], 'r').read())
    except (IOError, ValueError) as e:
        print 'Could not read', type, 'config file'
        print e
        return {}

def config_view(type):
    from flask import request, render_template, redirect

    assert type in ('pic', 'vid')
    if request.method == 'POST':
        conf = generate_conf(type, request.form)
        write_conf(type, conf)
        return redirect(request.path)
    config = read_conf(type)
    return render_template('camconfig.html', config=config, options=OPTIONS)

def reload_config():
    print 'Reloading config'
    for type in ('pic', 'vid'):
        conf = read_conf(type)
        current_confs[type] = list(chain(*conf.iteritems()))

def register_signal_handlers():
    signal.signal(signal.SIGUSR1, lambda *a: reload_config())

if __name__ == '__main__':
    for type in 'pic', 'vid':
        if read_conf(type):
            continue
        print 'Generating base', type, 'config'
        conf = generate_conf(type, {})
        write_conf(type, conf)
