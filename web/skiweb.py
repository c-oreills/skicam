import eventlet
eventlet.monkey_patch()

from sys import argv

from flask import Flask, redirect, render_template, request_started, url_for
from flask.ext.cache import Cache

from camconfig import config_view, set_parent
from pics import last_pics, pic_thumbnails_b64
from timeout import (reset_timeout, turn_on_wifi, terminate, init_timeout,
        disable_timeout)
from utils import get_disk_free

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '.cache'})

@app.route('/')
def index():
    thumb_pics = last_pics(10)
    pic = max(thumb_pics)
    thumbs = pic_thumbnails_b64(thumb_pics)
    disk_stats = get_disk_free()
    return render_template(
            'index.html', pic=pic, thumbs=thumbs, disk_stats=disk_stats)

@app.route('/pic_config', methods=('GET', 'POST'))
def pic_config():
    return config_view('pic')

@app.route('/vid_config', methods=('GET', 'POST'))
def vid_config():
    return config_view('vid')

@app.route('/kill')
def kill():
    terminate()

@app.route('/no_timeout')
def no_timeout():
    disable_timeout()
    return redirect(url_for('index'))


def reset_timeout_handler(s, **k):
    reset_timeout()
request_started.connect(reset_timeout_handler, app)

def register_parent():
    if len(argv) > 1:
        parent = argv[1]
    set_parent(parent)

if __name__ == '__main__':
    turn_on_wifi()
    init_timeout()
    register_parent()
    app.run(host='0.0.0.0', port=80, debug=True)
