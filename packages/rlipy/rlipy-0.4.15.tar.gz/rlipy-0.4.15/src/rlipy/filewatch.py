from . import env
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import re
from . import tradedate
import os
from . import htmlmail
from . import util
import rlipy.logger
import logging

def get_file_name(s):
    cal = tradedate.TradeDate('NOHOLIDAY')
    file_date = datetime.strftime(datetime.now(), '%Y%m%d')
    fn = re.sub('\$DATA', env.DATA_DIR, s['PATHNAME'])
    fn = re.sub('<today>', file_date, fn)
    fn = re.sub('<tomorrow>', cal.next_day_str(file_date), fn)
    fn = re.sub('<yesterday>', cal.previous_day_str(file_date), fn)
    return fn

def alert(s):
    under_watch = s['UNDER_WATCH']
    if(not under_watch):
        return
    cal = tradedate.TradeDate(s['CALENDER'])
    fn = s['PATHNAME']
    '''
    today = datetime.now()
    tomorrow = datetime.now()+timedelta(1)
    today_str = datetime.strftime(today,'%Y%m%d')
    tomorrow_str = datetime.strftime(tomorrow,'%Y%m%d')
    next_trade_date = cal.next_day_str(today_str)
    #no alert on Sunday if it's a today file
    if( (not cal.is_trade_day(today)) and re.search(today_str, fn)):
        return
    #no alert on friday if it's a tomorrow file 
    if(re.search(next_trade_date, fn) and tomorrow_str!=next_trade_date):
        return
    '''
    deadline = s['DEADLINE']
    now = datetime.strftime(datetime.now(), '%H:%M:%S')
    if(deadline<=now):
        if(not os.path.isfile(fn) or os.stat(fn).st_size<util.to_int(s['SIZE'])):
            email = ','.join([x+'@veritionfund.com' for x in re.split(',', s['EMAIL'])])
            msg = 'file: %s\nserver: %s\ncommand: %s' % (fn, s['SERVER'], s['COMMAND'])
            htmlmail.send(to_address=email, subject='file watch alert: missing '+s['DESCRIPTION'], body=msg)

def watch_today(s):
    today_weekday = datetime.today().weekday() #0 is monday; 6 is sunday
    today_weekday = '%d' % ((today_weekday+1)%7) #convert to crontab weekday
    try:
        str = s['WEEKDAYS']
        arr = str.split('|')
        return today_weekday in arr
    except:
        print("ERROR: failed to parse weekdays: %s" % str)
    return False
    
def get_deadline(s):
    dl = None
    try:
        dl = datetime.strftime(datetime.strptime(s['DEADLINE'], '%H:%M:%S'), '%H:%M:%S' )
        return dl
    except:
        print("ERROR: failed to get deadline \n%s" % (re.sub(';', '\n', s.to_string())))
        return ''
if __name__ == '__main__':
    src = env.ROOT_DIR+'/refdata/file_watch.csv'
    df = pd.read_csv(src)
    df['UNDER_WATCH'] = True
    df['UNDER_WATCH'] = df['UNDER_WATCH'] & (df.apply(watch_today, axis=1))
    df['DEADLINE'] = df.apply(get_deadline, axis=1)
    df = df[ (df['DEADLINE']!='') & (df['UNDER_WATCH'])]
    df = df.sort(['DEADLINE']).reset_index()
    df['PATHNAME'] = df.apply(get_file_name, axis=1)
    str = df[['PATHNAME', 'DEADLINE']].to_csv(sep='\t', index=False)
    logging.info('watching:\n%s' % (str))
    exit_time = df.iloc[-1]['DEADLINE']
    now = datetime.strftime(datetime.now(), '%H:%M:%S')
    while(True):
        df.apply(alert, axis=1)
        df = df[df['DEADLINE']>now]
        if(now>=exit_time):
            break
        time.sleep(60)
        now = datetime.strftime(datetime.now(), '%H:%M:%S')
        
        