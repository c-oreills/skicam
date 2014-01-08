from os import getpid
import subprocess

from capture import pic, vid


def play_sound(name):
    subprocess.Popen(['aplay', 'sounds/{n}.wav'.format(n=name)])

def capture_pic():
    pic()
    play_sound('camera')

def start_video():
    vid_p = vid()
    play_sound('whizfst2')

    def stop_video():
        vid_p.terminate()
        switch_menu(CAPTURE_MENU)

    switch_menu({'name': 'stop_vid', 'default': stop_video})

flask_p = None

def start_flask():
    global flask_p
    # Don't start multiple copies
    if flask_p and flask_p.poll() is None:
        return

    flask_p = subprocess.Popen(
            ['/home/pi/.virtualenvs/skicam/bin/python',
                '/home/pi/skicam/web/skiweb.py', str(getpid())],
            cwd='/home/pi/skicam/web/')
    play_sound('poweron')

SPEAK_IP_CMD = '''
ifconfig wlan0 |
grep -o "inet addr:[[:digit:]]\{1,3\}.[[:digit:]]\{1,3\}.[[:digit:]]\{1,3\}.[[:digit:]]\{1,3\}"
| espeak'''

def speak_ip():
    subprocess.Popen(SPEAK_IP_CMD, shell=True)

SPEAK_LAST_CAPTURE_CMD = 'ls DCIM -t | head -n 1 | espeak'

def speak_last_capture():
    subprocess.Popen(SPEAK_LAST_CAPTURE_CMD, shell=True)

CAPTURE_MENU = {
    'name': 'capture',
    'sound': 'computerbeep2',
    1: capture_pic,
    2: start_video,
    3: lambda: switch_menu(MUSIC_MENU),
    4: start_flask,
    5: speak_ip,
    6: speak_last_capture,
    7: lambda: switch_menu(SHUTDOWN_MENU),
    'eager_first': True,
}


def skip_track():
    subprocess.Popen(['mpc', 'next'])

def play_pause():
    subprocess.Popen(['mpc', 'toggle'])

MUSIC_MENU = {
    'name': 'music',
    'sound': 'computerbeep3',
    1: skip_track,
    2: play_pause,
    3: lambda: switch_menu(CAPTURE_MENU),
    4: start_flask,
}


def shutdown():
    play_sound('shutdowninprocess')
    subprocess.Popen(['halt'])

SHUTDOWN_MENU = {
    'name': 'shutdown',
    'sound': 'shutdowninprocess',
    'default': lambda: switch_menu(CAPTURE_MENU),
    3: shutdown,
}


current_menu = CAPTURE_MENU

def switch_menu(menu):
    global current_menu
    current_menu = menu
    sound = menu.get('sound')
    if sound:
        play_sound(sound)

def exec_menu_option(n, eager=False):
    # If eager_first is set, only exec option 1 if eager is True, and any other
    # number if eager is False
    if current_menu.get('eager_first', False):
        if eager:
            if n != 1:
                return
        else:
            if n == 1:
                return
    # Otherwise disregard eager calls
    elif eager:
        return

    fn = current_menu.get(n) or current_menu.get('default')
    if fn:
        fn()
