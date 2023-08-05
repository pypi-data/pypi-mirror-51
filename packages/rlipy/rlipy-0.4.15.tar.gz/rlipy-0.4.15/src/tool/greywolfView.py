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
import re
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user")
    parser.add_argument("-m", "--machine")
    parser.add_argument("-p", "--redis_server_port")
    args = parser.parse_args()
    redis_db = None
    if(args.redis_server_port):
        try:
            redis_port = int(args.redis_server_port)
            logging.info("connecting to redis %s %d" % ('vrnetf04', redis_port))
            redis_db = redis.StrictRedis('vrnetf04', redis_port)
        except:
            logging.error("failed to write to redis %s %d" % ('vrnetf04', redis_port))
    
    #dcohen_CT049-W10_greywolf_PositionWindow
    pattern = "/home/VERITIONFUND/rli/tmp/view/%s_%s_greywolf_*" % (args.user, args.machine)
    for fn in glob.glob(pattern):
        if(re.search("\.xml$", fn)):
            windowName = re.split('_',re.split('\.',fn)[0])[-1]
            redisKey = "HMDB:GREYWOLFVIEW:%s:%s" % (args.user, args.machine)
            with open(fn) as fh:
                content = fh.read()
                redis_db.hset(redisKey, windowName, content)
                logging.info("saved %s %s" % (redisKey, windowName) )

if __name__ == "__main__": main()