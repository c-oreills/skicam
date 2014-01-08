import subprocess

from flask import request

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    subprocess.Popen(['aplay', '../sounds/poweroff.wav'])
    func()

def get_disk_free():
    o = subprocess.check_output(['df', '-h', '/'])
    return o.split('\n')[1].split()[3:5]
