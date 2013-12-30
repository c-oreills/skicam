from base64 import b64encode
from collections import OrderedDict
from glob import glob
from itertools import islice

import exifread

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
    b64_thumbs = OrderedDict()
    for p in pics:
        bs = exifread.process_file(open(p, 'r'))['JPEGThumbnail']
        b64_thumbs[p] = 'data:image/jpeg;base64,' + b64encode(bs)
    return b64_thumbs
