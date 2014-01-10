from os import getpid
import subprocess

import capture
import pulser
import utils


def create_dialog(fn2, kwargs):
    def dialog():
        prompt = kwargs.pop('prompt', None)
        if prompt:
            prompt()
        prev_menu = current_menu
        dialog_menu = {
                2: fn2,
                'name': fn2.func_name,
                'default':  lambda: switch_menu(prev_menu)}
        dialog_menu.update(kwargs)
        switch_menu(dialog_menu)
    return dialog


def play_sound(name):
    subprocess.Popen(['aplay', 'sounds/{n}.wav'.format(n=name)])

def pic():
    capture.pic()
    play_sound('camera')

def start_video():
    vid_p = capture.vid()
    play_sound('whizfst2')
    pulser.set_pulse(30, lambda: play_sound('whizfst2'))

    def stop_video():
        vid_p.terminate()
        pulser.unset_pulse()
        switch_menu(MAIN_MENU)

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


playlist_n = 0
def next_playlist():
    global playlist_n
    playlists = subprocess.check_output(['mpc', 'lsplaylists']).split('\n')
    playlists.sort()
    playlists = filter(None, playlists)
    subprocess.Popen('mpc clear; mpc load {playlist}; mpc play'.format(playlist=playlists[playlist_n]), shell=True)
    playlist_n += 1
    playlist_n %= len(playlists)

def _mpc_command(*args):
    subprocess.Popen(('mpc',) + args)

def skip_track():
    _mpc_command('next')

def play_pause():
    _mpc_command('toggle')

def prev_track():
    _mpc_command('prev')

def volume_up():
    _mpc_command('volume', '+5')

def volume_down():
    _mpc_command('volume', '-5')

def toggle_single():
    _mpc_command('single')
    subprocess.Popen('mpc | grep -o "single: ..." | espeak', shell=True)

def toggle_random():
    _mpc_command('random')
    subprocess.Popen('mpc | grep -o "random: ..." | espeak', shell=True)

MAIN_MENU = {
    'name': 'main',
    'sound': 'computerbeep2',
    'eager_first': True,
    'eager_cleanup': capture.mark_last_rub,
    1: pic,
    2: start_video,
    3: lambda: switch_menu(MUSIC_MENU),
    4: play_pause,
    5: lambda: switch_menu(UTILS_MENU),
    6: start_flask,
}

MUSIC_MENU = {
    'name': 'music',
    'sound': 'computerbeep3',
    1: skip_track,
    2: next_playlist,
    3: lambda: switch_menu(MAIN_MENU),
    4: prev_track,
    5: lambda: switch_menu(MUSIC_MISC_MENU),
}

MUSIC_MISC_MENU = {
    'name': 'music',
    'sound': 'computerbeep1',
    1: volume_down,
    2: volume_up,
    3: lambda: switch_menu(MUSIC_MENU),
    4: toggle_random,
    5: toggle_single,
}


def silence_death():
    import main
    main.noisy_death = False

def halt():
    silence_death()
    play_sound('power_down_2')
    subprocess.Popen(['halt'])

def reboot():
    silence_death()
    play_sound('shutdowninprocess')
    subprocess.Popen(['reboot'])

def delete_rub():
    capture.delete_rub()
    play_sound('44')

UTILS_MENU = {
    'name': 'utils',
    'sound': 'computerbeep4',
    1: utils.speak_ip,
    2: utils.speak_last_capture,
    3: lambda: switch_menu(MAIN_MENU),
    4: create_dialog(reboot, {3: halt, 'sound': 'shutdowninprocess'}),
    5: create_dialog(delete_rub, {'prompt': utils.speak_rub_space}),
}


current_menu = MAIN_MENU

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
            eager_cleanup = current_menu.get('eager_cleanup')
            if eager_cleanup:
                eager_cleanup()
    # Otherwise disregard eager calls
    elif eager:
        return

    fn = current_menu.get(n) or current_menu.get('default')
    if fn:
        fn()
