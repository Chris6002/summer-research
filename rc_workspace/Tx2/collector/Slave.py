import time
from multiprocessing.connection import Listener
serv = Listener(('', 25000), authkey=b'peekaboo')

try:
    client = serv.accept()
    while True:
        starttime = time.time()
        msg = client.recv()
        print(time.time() - starttime)
finally:
    print('finished')