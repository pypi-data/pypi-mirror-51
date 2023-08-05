'''
Created on Nov 9, 2016

@author: rli
'''
import datetime
import logging
import os
import re
import subprocess
import time
import uuid
import pytz
from rlipy.env import  HMA_TODAY_DIR, HMA_TODAY_LINK
import pandas as pd


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return 0


def num(s):
    try:
        return float(s)
    except ValueError:
        return 0


def num_or_nah(s):
    try:
        return float(s)
    except ValueError:
        return None


def format_num(f):
    abs_val = abs(f)
    if(abs_val == 0):
        return '0'
    if(abs_val < 1):
        return '{:.4f}'.format(f)
    if(abs_val < 1000):
        return '{:.1f}'.format(f)
    if(abs_val < 1000000):
        return '{:,.0f}'.format(f)
    return '{:.2f}m'.format(f / 1000000.0)


def sync_run(cmd_and_arg):
    try:
        ret = re.split('\n', subprocess.check_output(cmd_and_arg, shell = True))
    except subprocess.CalledProcessError :
        # print "ERROR %s" % (e)
        return []
    return ret


def pandas_run(cmd_and_arg, sep = ' ', header = None):
    text_list = sync_run(cmd_and_arg)
    if(header is None):
        header = []
        if(len(text_list) == 0):
            return pd.DataFrame()
        header = re.split(sep, text_list.pop(0))
    tuple_list = []
    lnum = 0
    for line in text_list:
        lnum += 1
        if(len(line) == 0):
            continue
        tuples = re.split(sep, line)
        if(len(tuples) == len(header)):
            tuple_list.append(tuples)
        elif(len(tuples) > 0):
            logging.warning('pandas_run "%s" skip line#%d: %s', cmd_and_arg, lnum, line)
    if(len(tuple_list) == 0):
        return pd.DataFrame(columns = header)
    return pd.DataFrame(tuple_list, columns = header)


def tzdiff(timeZoneName):
    localTz = pytz.timezone("America/New_York")
    otherTz = pytz.timezone(timeZoneName)
    t = datetime.datetime(2019, 8, 7, 11, 0)
    localHour = t.astimezone(localTz).hour
    otherHour = t.astimezone(otherTz).hour
    return datetime.timedelta(0, (otherHour - localHour) * 3600)


def make_link(src, link):
    tmp = os.path.dirname(link) + '/' + str(uuid.uuid4())
    os.symlink(src, tmp)
    os.rename(tmp, link)


def hma_make_today_dir():
    try:
        os.umask(000)
        os.makedirs(HMA_TODAY_DIR)
        make_link(HMA_TODAY_LINK, HMA_TODAY_DIR)
        os.chmod(HMA_TODAY_DIR, 0o775)
    except FileExistsError:
        pass

