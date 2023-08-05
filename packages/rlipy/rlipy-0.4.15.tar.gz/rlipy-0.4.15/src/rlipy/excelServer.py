from datetime import datetime
from enum import Enum
import copy
import logging
import re
import time

import zmq

import rlipy.subscriptionManager as subscriptionManager
import rlipy.zpub as zpub
import rlipy.zpull as zpull


class SubscribeMsgField(Enum):
    msgType = 0
    msgCategory = 1
    symbol = 2


class ExcelServer:

    def __init__(self, name, jsonConfig, dataFeed):
        self.jsonConfig = jsonConfig
        self.name = name
        self.datafeed = dataFeed
        self.cache = {}  # map symbol to data
        self.sentMsgNo = 0
        self.sentMsgLastLoop = 0
        self.clientMsg = ''

        self.loadYesterdaySubscription()
        self.setEndTime(jsonConfig)
        self.setSockets(jsonConfig)

    def loadYesterdaySubscription(self):
        self.subscriptions = subscriptionManager.RedisSubscriptionManager(
            self.name, self.jsonConfig["redisHost"], int(self.jsonConfig["redisPort"]))

    def setEndTime(self, jsonConfig):
        tmp = datetime.strptime(jsonConfig['endTime'], "%H:%M:%S")
        now = datetime.now()
        self.endTime = datetime(now.year, now.month, now.day, tmp.hour, tmp.minute, tmp.second)

    def setSockets(self, jsonConfig):
        self.subscribeAddress = jsonConfig['subscribeAddress']
        self.publishAddress = jsonConfig['publishAddress']
        self.zcontext = zmq.Context()
        self.subSocket = zpull.zpull(self.zcontext, self.subscribeAddress)
        self.pubSocket = zpub.zpub(self.zcontext, self.publishAddress)
        logging.info("server %s bind subscribe socket to %s", self.name, self.subscribeAddress)
        logging.info("server %s bind publish socket to %s", self.name, self.publishAddress)

    def shutDown(self):
        logging.info("shutting down server")
        logging.info("stat: sentMsgNo=%d, cache=%d, subscribed=%d",
            self.sentMsgNo, len(self.cache), len(self.subscriptions.getAllSymbols()))
        self.subSocket.close()
        self.pubSocket.close()
        self.datafeed.shutDown()
        logging.info("server is down")

    def run(self):
        logging.debug("starting excelserver")
        self.getSnapshotForYesterdaySymbols()
        self.loop()

    def getSnapshotForYesterdaySymbols(self):
        for symbol in self.subscriptions.getAllSymbols():
            self.subscribeToDataFeed(symbol)
        updates = self.datafeed.getAll()
        for update in updates:
            self.onData(update)

    def loop(self):
        logging.info("start looping")
        while datetime.now() < self.endTime:
            try:
                self.pollClients()
                self.pollPriceFeeds()
                self.sleepIfNoNewData()
            except KeyboardInterrupt:
                logging.info("KeyboardInterrupt. exiting...")
                break
            except:
                logging.error("main loop fails", exc_info = True)

    def pollClients(self):
        self.clientMsg = self.subSocket.recv()
        while(self.clientMsg):
            self.clientMsg = self.clientMsg.decode('ascii')
            logging.debug("recv msg from client: %s", self.clientMsg)
            try:
                tokens = re.split(r'\|', self.clientMsg)
                self.parseClientMessage(tokens)
            except:
                logging.error("%s failed to parse msg %s", self.name, self.clientMsg,
                                  exc_info = True)
                continue
            self.clientMsg = self.subSocket.recv()

    def parseClientMessage(self, tokens):
        if (tokens[SubscribeMsgField.msgType.value] == 'R'):
            if (tokens[SubscribeMsgField.msgCategory.value] == 'S'):
                symbol = tokens[SubscribeMsgField.symbol.value]
                self.subscribe('', symbol)
            elif (tokens[SubscribeMsgField.msgCategory.value] == 'U'):
                symbol = tokens[SubscribeMsgField.symbol.value]
                self.unsubscribe('', symbol)

    def subscribe(self, client, symbol):
        if(not self.subscriptions.hasSymbol(symbol)):
            self.subscribeToDataFeed(symbol)
        elif(symbol in self.cache):
            logging.debug("snapshot %s", str(self.cache[symbol]))
            self.publishData(self.cache[symbol])
        self.subscriptions.addSymbol(symbol, client)

    def publishData(self, data):
        self.pubSocket.send(('M|U|' + str(data)).encode('ascii'))
        self.sentMsgNo += 1

    def subscribeToDataFeed(self, symbol):
        logging.debug("subscribeToDataFeed %s ", symbol)
        self.datafeed.subscribe(symbol)

    def unsubscribe(self, client, symbol):
        logging.debug("unsubscribe %s from %s", symbol, client)
        self.subscriptions.removeSymbol(symbol, client)

    def pollPriceFeeds(self):
        for update in self.datafeed.getUpdates():
            self.onData(update)

    def onData(self, data):
        # logging.debug("onData %s", str(data)))
        old = self.cache[data.symbol] if data.symbol in self.cache else None
        sameData = (old != None and old == data)
        if(old is None):
            self.cache[data.symbol] = copy.copy(data)
        else:
            self.cache[data.symbol].merge(data)
        if((not self.subscriptions.hasSymbol(data.symbol)) or sameData):
            return
        logging.debug("publish %s", str(self.cache[data.symbol]))
        self.publishData(self.cache[data.symbol])

    def sleepIfNoNewData(self):
        if (self.sentMsgLastLoop == self.sentMsgNo):
            time.sleep(1)
        else:
            self.sentMsgLastLoop = self.sentMsgNo
