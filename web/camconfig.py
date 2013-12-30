from itertools import izip_longest


BASE_CMD_STILL = """#!/bin/bash
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
    'pic': BASE_CMD_STILL,
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


def generate_cmd(type, ex=None):
    cmd = BASE_CMDS[type]
    if ex and ex in OPTIONS['--exposure']:
        cmd += ' --exposure ' + ex
    return cmd

def write_cmd(type, cmd):
    open(CMD_FILES[type], 'w').write(cmd)

def read_cmd(type):
    cmd = open(CMD_FILES[type], 'r').read()
    # Strip off base and leading space
    cmd = cmd[len(BASE_CMDS[type]) + 1:]

    if not cmd:
        return {}

    cmd = cmd.split()
    cmd_kwargs = {k: v for k, v in grouper(cmd, 2) if k in OPTIONS}
    return cmd_kwargs
