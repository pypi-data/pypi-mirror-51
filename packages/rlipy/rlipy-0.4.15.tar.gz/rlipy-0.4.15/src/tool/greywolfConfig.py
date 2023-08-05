'''
Created on Apr 26, 2017
@author: rli
'''

import os
import datetime
import pandas as pd
import argparse
import re
import traceback
import redis
import logging
import json
import math
import rlipy.util as util
import rlipy.logger
import glob

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fromRedisKey")
    parser.add_argument("toRedisKey")
    parser.add_argument("-t", "--newTicker", default="")
    parser.add_argument("-a", "--newAccount", default="")
    parser.add_argument("-p", "--redis_server_port")
    args = parser.parse_args()
    nowStr = datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')
    redisDb = None
    if(args.redis_server_port):
        try:
            redis_port = int(args.redis_server_port)
            redisDb = redis.StrictRedis('vrnetf04', redis_port)
        except:
            logging.error("failed to write to redis %s %d" % ('vrnetf04', redis_port))
    try:
        redisDb.rename(args.toRedisKey, args.toRedisKey+"."+nowStr)
    except:
        pass
    j = redisDb.get(args.fromRedisKey)
    j = json.loads(j)
    if(args.newTicker):
        j['Ticker'] =  args.newTicker
    if(args.newAccount):
        j['Account'] =  args.newAccount
    redisDb.set(args.toRedisKey, json.dumps(j))
    logging.error("create %s from %s" % (args.toRedisKey, args.fromRedisKey))
                                  
if __name__ == "__main__": 
    main()