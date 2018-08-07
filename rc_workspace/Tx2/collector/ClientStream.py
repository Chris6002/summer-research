class ClientStream:
    def __init__(self,server):
        self.server =server
        self.started = False
        self.read_lock = Lock()

    def start(self):
        while True:
            self.client=self.server.accept()
            if self.started:
                print("already started!!")
                return None
            self.started = True
            self.thread = Thread(target=self.update, args=()).start()
        
        return self

    def update(self):
        while self.started:
            try:
                msg = self.client.recv().split(':')
                self.read_lock.acquire()
                self.msg = msg
                self.read_lock.release()
            except:
                client.close()
                return False


    def read(self):
        self.read_lock.acquire()
        msg = self.msg.copy()
        self.read_lock.release()
        return msg

    def stop(self):
        self.started = False
        self.thread.join()