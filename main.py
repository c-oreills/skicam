from os import chdir
from time import sleep, time

from RPi import GPIO

from menus import exec_menu_option
from web.camconfig import reload_config, register_signal_handlers

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

TOGGLE_TIMEOUT = 0.5
TOGGLE_POLL = 0.05
TOGGLE_REPEAT_POLL = 0.01

DEBUG = True


def read_input():
    return GPIO.input(3)

def poll_toggles():
    last_val = read_input()
    last_toggle_time = time()
    toggle_count = 0

    def poll_sleep():
        sleep_time = TOGGLE_REPEAT_POLL if toggle_count else TOGGLE_POLL
        sleep(sleep_time)

    while True:
        t = time()
        if toggle_count and t - last_toggle_time > TOGGLE_TIMEOUT:
            exec_menu_option(toggle_count)
            if DEBUG:
                print 'Toggled', toggle_count, 'times'
            toggle_count = 0

        val = read_input()
        if val == last_val:
            poll_sleep()
            continue

        last_val = val

        toggle_count += 1
        # Trigger the first option instantly if it's set to eager
        exec_menu_option(toggle_count, eager=True)

        last_toggle_time = time()
        poll_sleep()

def run():
    chdir('/home/pi/skicam')
    reload_config()
    register_signal_handlers()
    poll_toggles()

def run_daemon():
    import daemon
    logfile = open('/home/pi/skicam/ski.log', 'a+')
    with daemon.DaemonContext(stdout=logfile, stderr=logfile):
        run()


if __name__ == '__main__':
    run_daemon()
