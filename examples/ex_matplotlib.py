import sys
sys.path.insert(0, '..')
import time
import threading
from crew.metrics.httpapi import HttpAPI


# XXX The test script needs matplotlib


def f():
    # create the api object.
    api = HttpAPI(namespace='ns', apikey='apikey', hostname='localhost',
        port=2000, timeout=20)
    # set the start and end range. Not implemented yet.
    start_time = time.time() - 100000
    end_time = time.time()
    # Do a retrieve and display the graph.
    for _ in range(1):
        x = api.retrieve(start_time=start_time, end_time=end_time, interval=1,
            attributes={'type': 'E'},
            fields=['amount'])
        print x
#        test_plot(x)
        print len(x)


def test_plot(x):
    import matplotlib.pyplot as plt
    times = [y['timestamp'] for y in x]
    amounts  = [y['amount'] for y in x]
    z = plt.plot(times, amounts, 'g^-')
    plt.show()


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
