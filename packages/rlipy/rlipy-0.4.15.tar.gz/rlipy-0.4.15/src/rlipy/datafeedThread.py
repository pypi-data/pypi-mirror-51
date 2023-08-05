from queue import Queue, Empty
import logging
import threading

from . import datafeed


class DataFeedThread(datafeed.DataFeedBase):

    def __init__(self, datafeedImpl):
        self.datafeedImpl = datafeedImpl
        self.subscribeQueue = Queue()
        self.updateQueue = Queue()
        self.killed = False
        self.thread = threading.Thread(target = self.run)
        self.thread.start()
        self.recvUpdateCount = 0
        self.sendUpdateCount = 0

    def subscribe(self, symbol):
        self.subscribeQueue.put(symbol)

    def getAll(self):
        return self.datafeedImpl.getAll()

    def getUpdates(self):
        updates = []
        try:
            while(not self.updateQueue.empty()):
                u = self.updateQueue.get()
                logging.debug("update %s", u)
                updates.append(u)
                self.sendUpdateCount += 1
        except Empty:
            pass
        return updates

    def shutDown(self):
        self.killed = True

    def processSubscribes(self):
        try:
            while True:
                newSubscribe = self.subscribeQueue.get(timeout = 1)
                self.datafeedImpl.subscribe(newSubscribe)
        except Empty:
            pass

    def run(self):
        while(not self.killed):
            try:
                self.processSubscribes()
                updates = self.datafeedImpl.getUpdates()
                for u in updates:
                    self.updateQueue.put(u)
                    logging.debug("update %s", u)
                    self.recvUpdateCount += 1
                if(updates):
                    logging.info("recv update %d sent %d", self.recvUpdateCount, self.sendUpdateCount)
            except :
                logging.error("DataFeedThread main loop error", exc_info = True)

