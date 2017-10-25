"""
Demo of a debounce method that's reasoanbly efficient with threads. It still
needs to create and end threads, otherwise the interpreter will hang, but
doesn't cancel and re-create threads if there are no more remaining.
"""
import functools
import threading
import time


class DebounceThread(threading.Thread):
    def __init__(self, interval, function):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.all_args = []
        self.reset_timer_event = threading.Event()

    @property
    def finished(self):
        return not self.all_args

    def enqueue(self, args):
        self.all_args.append(args)
        self.reset_timer_event.set()

    def run(self):
        while True:
            self.reset_timer_event.wait(self.interval)
            if self.all_args and not self.reset_timer_event.is_set():
                self.function(self.all_args)
                del self.all_args[:]
                return
            self.reset_timer_event.clear()


def debounce(interval):
    def wrapper(fcn):
        debounce_thread = [None]  # Cleaner with `nonlocal` keyword in python 3
        def fcn_helper(*args):
            if (not debounce_thread[0]) or debounce_thread[0].finished:
                debounce_thread[0] = DebounceThread(interval, fcn)
                debounce_thread[0].start()
            debounce_thread[0].enqueue(args)
        return fcn_helper
    return wrapper


@debounce(1.0)
def test_fcn(all_args):
    print("New batch")
    for x, y in all_args:
        print("    {}, {}".format(x, y))


for i in xrange(9):
    test_fcn('batch1', i)
    time.sleep(0.1)
time.sleep(0.95)
test_fcn('batch2', 'y')
time.sleep(2.01)
