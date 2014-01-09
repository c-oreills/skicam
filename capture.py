from glob import glob
import subprocess

from web.camconfig import current_confs


last_pic_proc = None

def _wait_on_last_pic():
    if last_pic_proc:
        last_pic_proc.wait()

def _format_n(n, ext):
    return 'DCIM/{n:05}.{ext}'.format(n=n, ext=ext)


def pic():
    global last_pic_proc
    _wait_on_last_pic()
    last_pic_proc = subprocess.Popen(
            ['raspistill', '-o', _format_n(next_pic_n(), ext='jpg'),
                '-t', '10'] + current_confs['pic'])

def vid():
    _wait_on_last_pic()
    return subprocess.Popen(
            ['raspivid', '-o', _format_n(next_pic_n(), ext='h264'),
                '-t', '99999999'] + current_confs['vid'])


def _last_pic_n(ext='jpg'):
    all_pics = glob('DCIM/*.{ext}'.format(ext=ext))
    if not all_pics:
        return 0
    last_pic = max(all_pics)
    last_pic_n = last_pic[last_pic.find('/')+1:last_pic.find('.')]
    return int(last_pic_n)

def get_last_pic_n():
    return max(_last_pic_n(), _last_pic_n('h264'))

last_pic_n = get_last_pic_n()

def next_pic_n():
    global last_pic_n
    last_pic_n += 1
    return last_pic_n

def mark_last_rub():
    subprocess.Popen('sleep 3; mv {pic} {rub}'.format(
        pic=_format_n(last_pic_n, ext='jpg'),
        rub=_format_n(last_pic_n, ext='jpg.rub')), shell=True)

def delete_rub():
    subprocess.Popen('rm DCIM/*.rub', shell=True)
