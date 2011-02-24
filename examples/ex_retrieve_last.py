import sys
sys.path.insert(0, '..')
from crew.metrics.httpapi import HttpAPI


def main():
    # See ex_create.py
#    api = HttpAPI(namespace='ns', apikey='apikey', hostname='localhost',
#        port=2000, timeout=20)
#    print api.retrieve_last(attributes={'type': 'A'}, limit=2)
#    print api.retrieve_last(attributes={'type': 'A'}, limit=3)
#    print api.retrieve_last(attributes={'type': ['A', 'B']}, limit=5)
    api = HttpAPI(namespace='windows', apikey='apikey', hostname='129.10.112.144',
        port=2000, timeout=20)
    print api.retrieve_last(attributes={'hostname': 'bulbasaur'})


if __name__ == '__main__':
    main()
