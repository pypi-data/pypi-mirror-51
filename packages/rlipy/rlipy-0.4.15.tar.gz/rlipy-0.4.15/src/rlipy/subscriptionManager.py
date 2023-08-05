import datetime
import redis
import logging
from . import logger
logger = logging.getLogger(__name__)
class SubscriptionManager(object):
    def __init__(self):
        self.symbols = set()
        self.symbol2Clients = {}
        self.client2Symbols = {}
        
    def getAllSymbols(self):
        return sorted(list(self.symbol2Clients.keys()))
    
    def getClientSymbols(self, client):
        if(client in self.client2Symbols):
            return sorted(list(self.client2Symbols[client]))
        else:
            return []
    
    def hasSymbol(self, symbol):
        return symbol in self.symbol2Clients    
            
    def removeSymbol(self, symbol, client):
        if(client in self.client2Symbols):
            if(symbol in self.client2Symbols[client]):
                 self.client2Symbols[client].remove(symbol)
        
        if(symbol in self.symbol2Clients):
            if(client in self.symbol2Clients[symbol]):
                 self.symbol2Clients[symbol].remove(client)
                     
    def addSymbol(self, symbol, client):
        if(not symbol in self.symbol2Clients):
            self.symbol2Clients[symbol] = set()
        if(not client in self.symbol2Clients[symbol]):
            self.symbol2Clients[symbol].add(client)

        if(not client in self.client2Symbols):
            self.client2Symbols[client] = set()
        if(not symbol in self.client2Symbols[client]):
            self.client2Symbols[client].add(symbol)
            

class RedisSubscriptionManager(SubscriptionManager):

    def getTodaySubAndRemoveStaleFromRedis(self):
        subs = self.redis_db.hgetall(self.redisKey)
        stale = []
        for symbol, subDate in list(subs.items()):
            if (subDate < self.today):
                stale.append(symbol)
        for s in stale: #remove stale subscriptions from redis
            del subs[s]
            self.redis_db.hdel(self.redisKey, s)
        return  subs

    def __init__(self,  name, redisHost, redisPort):
        super(RedisSubscriptionManager, self).__init__()
        self.name = name
        self.today =  datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
        try:
            self.host = redisHost
            self.port = redisPort
            logger.info("connecting to redis %s %d" % (self.host, self.port))
            self.redis_db = redis.StrictRedis(self.host, self.port, charset="ascii",  decode_responses=True)
        except:
            logger.error("failed to connect to redis %s %d" % (self.host, self.port))
            raise
        self.redisKey = "PRICEFEED:"+name+":SUB"
        logger.info("%s use redis key %s" % (self.name, self.redisKey))
        subs = self.getTodaySubAndRemoveStaleFromRedis()
        for symbol, subDate in list(subs.items()):
            #logger.debug("subscription from redis %s", symbol)
            super(RedisSubscriptionManager, self).addSymbol(symbol, '')
        logger.info("loaded %d symbols", len(self.symbol2Clients))
        
    def addSymbol(self, symbol, client):
        existing = self.hasSymbol(symbol)
        super(RedisSubscriptionManager, self).addSymbol(symbol, client)
        if(not existing):
            self.redis_db.hset(self.redisKey, symbol, self.today)
            