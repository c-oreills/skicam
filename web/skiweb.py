from base64 import b64encode
from collections import OrderedDict
from glob import glob
from itertools import islice
import subprocess

import exifread
from flask import Flask, render_template

app = Flask(__name__)

def last_pics(n=1):
    all_pics = glob('static/DCIM/*.jpg')
    if not all_pics:
        return
    if n == 1:
        return max(all_pics),
    return tuple(islice(sorted(all_pics, reverse=True), n))

def last_pic():
    p = last_pics()
    if not p:
        return
    p, = p
    return p

def pic_thumbnails_b64(pics):
    b64_thumbs = {}
    for p in pics:
        bs = exifread.process_file(open(p, 'r'))['JPEGThumbnail']
        b64_thumbs[p] = 'data:image/jpeg;base64,' + b64encode(bs)
    return b64_thumbs

def get_disk_free():
    o = subprocess.check_output(['df', '-h', '/'])
    return o.split('\n')[1].split()[3:5]

@app.route('/')
def index():
    thumb_pics = last_pics(10)
    pic = max(thumb_pics)
    thumbs = pic_thumbnails_b64(thumb_pics)
    disk_stats = get_disk_free()
    return render_template(
            'index.html', pic=pic, thumbs=thumbs, disk_stats=disk_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
