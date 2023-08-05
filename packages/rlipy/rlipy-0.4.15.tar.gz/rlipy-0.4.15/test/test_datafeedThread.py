import time
import rlipy.datafeedThread as datafeedThread


class FakeDataFeed:

    def __init__(self):
        self.seqNo = 0
        self.batchSize = 10000

    def getUpdates(self):
        updates = list(range(self.seqNo, self.seqNo + self.batchSize))
        self.seqNo += self.batchSize
        return updates

    def subscribe(self):
        pass


def createDataFeedThreadAndRun3Second():
    feedThread = datafeedThread.DataFeedThread(FakeDataFeed())
    time.sleep(3)
    feedThread.shutDown()
    time.sleep(1)
    return feedThread


def test_getUpdate():
    feedThread = createDataFeedThreadAndRun3Second()
    updates = feedThread.getUpdates()
    assert(len(updates) == feedThread.recvUpdateCount)
