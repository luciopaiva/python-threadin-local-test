"""
Experiment to validate what happens when you subclass threading.local.

The method dump() will be called print the address of ``my`` and ``my.x`` once for every thread in that thread's
context. You will see that the address of ``my`` doesn't change at all among thread contexts. Only the address of
``my.x`` will change, showing that internally Python is instantiating only MyLocal's attributes, but not MyLocal
itself.
"""

from functools import partial
from concurrent.futures import ThreadPoolExecutor, wait
import threading
import time


def dump():
    """

    """
    print('\t@(my) = 0x{:0X} | @(x) = 0x{:0X} | x = {}'.format(id(my), id(my.x), my.x))


def run(index):
    time.sleep(0.2)
    my.x = index
    dump()


class MyLocal(threading.local):

    def __init__(self):
        self.x = 42

# The constructor should be called only once throught all execution:
my = MyLocal()

# my.x initial value on main thread:
dump()

t = threading.Thread(target=partial(run, 43))
t.start()
t.join()

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []
    for i in range(10):
        futures.append(executor.submit(run, i))
    wait(futures)

# my.x initial value remains the same on main thread:
dump()
assert my.x == 42
