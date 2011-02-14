import sys
sys.path.insert(0, '..')
import time
import threading
from crew.metrics.httpapi import HttpAPI
from random import randint

# Shows how to insert data.

def f():
    # Create the api object.
    api = HttpAPI(namespace='ns', apikey='apikey', hostname='localhost',
        port=2000, timeout=20)
    # For n (100) times insert some data.
    start = time.time() - 1000
    for i in range(100):
        # timestamp denotes when the event occured.
        api.store(timestamp=start + i, **{
            'amount': randint(0, 5000),
            'type': 'E',
#            'type': randint(0, 2) and 'A' or 'B',
        })


def main():
    ts = []
    for _ in range(1):
        t = threading.Thread(target=f)
        t.daemon = True
        t.start()
        ts.append(t)
    for t in ts:
        t.join()


if __name__ == '__main__':
    main()
