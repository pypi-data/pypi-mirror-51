'''
Created on Nov 4, 2016

@author: rli
'''
from datetime import datetime
import os
import sys

BBQ_HOST = 'rli02-w7'
BBQ_PORT = '7200'
BBQ_PORT_2 = '5555'
BBQ_PORT_3 = '5555'

IS_WINDOWS = sys.platform.find('win') == 0
if(IS_WINDOWS):
    DATA_DIR = 'R:'
else:
    DATA_DIR = '/data'
ROOT_DIR = os.path.join(DATA_DIR, 'prod', 'infra')
SECMAST_DIR = os.path.join(ROOT_DIR, 'secmast')

HMA_DAILY_DIR = os.path.join(DATA_DIR, 'prod', 'hma', 'daily')
HMA_TODAY_DIR = os.path.join(HMA_DAILY_DIR, datetime.strftime(datetime.now(), '%Y%m%d'))
HMA_TODAY_LINK = os.path.join(HMA_DAILY_DIR, 'today')
