import time
from multiprocessing.connection import Client

record_FPS = 10
c = Client(('localhost', 25000), authkey=b'peekaboo')
try:
    starttime = time.time()

    while True:
        starttime = time.time()
        c.send('hello')
        time.sleep(1 / record_FPS - (
            (time.time() - starttime) % (1 / record_FPS)))
        print(time.time() - starttime)
finally:
    print('finished')
