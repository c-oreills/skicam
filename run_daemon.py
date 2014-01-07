from daemon import DaemonContext

def run_daemon():
    logfile = open('/home/pi/skicam/ski.log', 'a+')
    with DaemonContext(working_directory='/home/pi/skicam', stdout=logfile, stderr=logfile):
        from main import run
        run()

if __name__ == '__main__':
    run_daemon()
