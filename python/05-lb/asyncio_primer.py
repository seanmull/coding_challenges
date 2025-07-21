#!/usr/bin/env python3

import scheduler.trigger as trigger
from scheduler import Scheduler
import datetime as dt
from time import sleep


def add_one():
    x = 0
    while True:
        x += 1
        yield x
        sleep(1)


def filter_even():
    while True:
        x = yield
        if x % 2 == 0:
            print(x)


filter = filter_even()
generator = add_one()
filter.send(None)

# for val in generator:
#     filter.send(val)


def foo():
    print("foo")

# schedule = Scheduler()
# schedule.cyclic(dt.timedelta(seconds=1), foo)

# while True:
    # schedule.exec_jobs()


def ping():
    print("ping")
    sleep(1)


def pong():
    print("pong")
    sleep(1)


# pass threads if we want to do this in parrellel
schedule = Scheduler(n_threads=0)
schedule.cyclic(dt.timedelta(), ping)
schedule.cyclic(dt.timedelta(), pong)

# while True:
# schedule.exec_jobs()
