pulse_polls = None
pulse_fn = None
poll_count = 0

def set_pulse(s, fn):
    global pulse_polls, pulse_fn
    import main
    pulse_polls = s / float(main.TOGGLE_POLL)
    pulse_fn = fn

def unset_pulse():
    global pulse_polls, pulse_fn
    pulse_polls = None
    pulse_fn = None
