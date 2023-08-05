import logging
import redis
class RedisConn(object):
    def __init__(self, host, port,):
        try:
            self.host = host
            self.port = port
            logging.info("connecting to redis %s %d" % (host, port))
            self.redis_db = redis.StrictRedis(host, port)
        except:
            logging.error("failed to connect to redis %s %d" % (host, port))
            raise
    
    def executeCommand(self, cmd):
        return self.redis_db.execute_command(cmd)