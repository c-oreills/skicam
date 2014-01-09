import subprocess


SPEAK_IP_CMD = '''
ifconfig wlan0 |
grep -o "inet addr:[[:digit:]]\{1,3\}.[[:digit:]]\{1,3\}.[[:digit:]]\{1,3\}.[[:digit:]]\{1,3\}" |
espeak'''

def speak_ip():
    subprocess.Popen(SPEAK_IP_CMD, shell=True)

SPEAK_LAST_CAPTURE_CMD = 'ls DCIM -t | head -n 1 | espeak'

def speak_last_capture():
    subprocess.Popen(SPEAK_LAST_CAPTURE_CMD, shell=True)

SPEAK_RUB_SPACE_CMD = 'du -hc DCIM/*.rub | tail -n 1 | espeak'

def speak_rub_space():
    subprocess.Popen(SPEAK_RUB_SPACE_CMD, shell=True)
