import subprocess
from time import sleep, time

from RPi import GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN)

TOGGLE_TIMEOUT = 0.5
TOGGLE_POLL = 0.05
TOGGLE_REPEAT_POLL = 0.01

DEBUG = True


def pic():
    print 'pic'
    subprocess.call(['raspistill', '-o', 'DCIM/img.jpg', '-t', '100'])

def start_video():
    print 'start vid'
    pass

def stop_video():
    print 'stop vid'
    pass

def kill_flask():
    print 'kill flask'
    pass

def start_flask():
    print 'start flask'
    pass


TOGGLE_FNS = {
    1: pic,
    3: start_video,
    4: kill_flask,
    5: start_flask,
}


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
            toggle_fn = TOGGLE_FNS.get(toggle_count)
            if toggle_fn:
                toggle_fn()
            if DEBUG:
                print 'Toggled', toggle_count, 'times'
            toggle_count = 0

        val = read_input()
        if val == last_val:
            poll_sleep()
            continue

        last_val = val

        toggle_count += 1
        # Always trigger first toggle
        if toggle_count == 1:
            TOGGLE_FNS[1]()

        last_toggle_time = time()
        poll_sleep()

def run():
    poll_toggles()

def run_daemon():
    import daemon
    with daemon.DaemonContext():
        run()
