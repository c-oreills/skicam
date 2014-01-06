from itertools import izip_longest

from flask import request, render_template, redirect


BASE_CMD_PIC = """#!/bin/bash
raspistill -o DCIM/$1.jpg -t 0 -rot 180"""

BASE_CMD_VID = """#!/bin/bash
raspivid -o DCIM/$1.h264 -t 99999999 -rot 180"""

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

BASE_CMDS = {
    'pic': BASE_CMD_PIC,
    'vid': BASE_CMD_VID
}

CMD_FILES = {
    'pic': '../run_raspistill',
    'vid': '../run_raspivid'
}


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def generate_cmd(type, config):
    cmd = BASE_CMDS[type]
    for k, v in config.iteritems():
        if v in OPTIONS.get(k, {}):
            cmd += ' ' + k + ' '  + v
    return cmd

def write_cmd(type, cmd):
    open(CMD_FILES[type], 'w').write(cmd)

def read_cmd(type):
    try:
        cmd = open(CMD_FILES[type], 'r').read()
    except IOError:
        return {}

    # Strip off base and leading space
    cmd = cmd[len(BASE_CMDS[type]) + 1:]

    if not cmd:
        return {}

    cmd = cmd.split()
    config = {k: v for k, v in grouper(cmd, 2) if k in OPTIONS}
    return config

def config_view(type):
    assert type in ('pic', 'vid')
    if request.method == 'POST':
        cmd = generate_cmd(type, request.form)
        write_cmd(type, cmd)
        return redirect(request.path)
    config = read_cmd(type)
    return render_template('camconfig.html', config=config, options=OPTIONS)
