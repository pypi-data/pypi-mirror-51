import os
import datetime
import sys
import dateutil.rrule as dr
import dateutil.relativedelta as drel
import pandas as pd
import logging
def today():
    return datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
class TradeDate(object):      
    def __init__(self, market='NOHOLIDAY'):
        self.holidays = set()
        self.weekend = [5,6]
        if(market=='NOHOLIDAY'):
            return
        holiday_file_dir = '/data/prod/infra/refdata/holiday/'
        if(not os.path.isdir(holiday_file_dir)):
            holiday_file_dir = os.environ['HOLIDAY_FILE_DIR']
        holiday_file_path = holiday_file_dir + market + '.txt'
        if(market=='cme'):
            holiday_file_path = holiday_file_dir + 'nyse' + '.txt'
        if(not os.path.isfile(holiday_file_path)):
            logging.error("can't find holiday file %s" % (holiday_file_path))
            return
        file = open(holiday_file_path, 'r')
        for line in file:
            holiday = datetime.datetime.strptime(line.rstrip('\n'), '%Y%m%d')
            self.holidays.add(holiday)
        if(market=='cme'):
            self.weekend = [5]
            
    def is_trade_day(self, day):
        day_ = datetime.datetime.combine(day, datetime.datetime.min.time())
        if(day_.weekday() in self.weekend):
            return False
        if(day_ in self.holidays):
            return False
        return True 
    
    def get_month_option_expiration(self, day_str, day_str_format = '%Y%m%d'):
        day = datetime.datetime.strptime(day_str, day_str_format);
        rr = dr.rrule(dr.MONTHLY,byweekday=drel.FR(3), count=1, dtstart=datetime.datetime(day.year, day.month, 1))
        third_friday = rr[0]
        expire_day = third_friday
        if(not self.is_trade_day(third_friday)):
            expire_day = self.previous_day(third_friday)
        return datetime.datetime.strftime(expire_day, day_str_format)
    
    def _get_last_day_in_month(self, day_str, day_str_format = '%Y%m%d'):
        day = datetime.datetime.strptime(day_str, day_str_format)
        rr = dr.rrule(dr.MONTHLY,bymonthday=-1, count=1, dtstart=datetime.datetime(day.year, day.month, 1))
        month_end = rr[0]
        if(not self.is_trade_day(month_end)):
            month_end = self.previous_day(month_end)
        return datetime.datetime.strftime(month_end, day_str_format)
        
    def next_day(self, day):
        _day = day + datetime.timedelta(days=1)
        while not self.is_trade_day(_day):
            _day += datetime.timedelta(days=1)
        return _day
    
    def day_str_diff(self, day1_str, day2_str, day_str_format = '%Y%m%d'):
        day1 = datetime.datetime.strptime(day1_str, day_str_format);
        day2 = datetime.datetime.strptime(day2_str, day_str_format);
        n = 0;
        while(day1!=day2):
            if(day1>day2):
                n += 1
                day1 = self.previous_day(day1)
            else:
                n -= 1
                day1 = self.next_day(day1)
        return n;
    
    def next_day_str(self, day_str, day_str_format = '%Y%m%d'):
        day = datetime.datetime.strptime(day_str, day_str_format);
        return datetime.datetime.strftime(self.next_day(day), day_str_format)
        
    def previous_day(self, day):
        _day = day - datetime.timedelta(days=1)
        while not self.is_trade_day(_day):
            _day -= datetime.timedelta(days=1)
        return _day
    
    def previous_day_str(self, day_str, day_str_format = '%Y%m%d'):
        day = datetime.datetime.strptime(day_str, day_str_format);
        return datetime.datetime.strftime(self.previous_day(day), day_str_format)
       
    def next_n_days(self, day, n):
        ndays = []
        _day = day
        while len(ndays)<n:
            _day = self.next_day(_day)
            ndays.append(_day)
        ndays.sort();
        return ndays
    
    def previous_n_days(self, day, n):
        ndays = []
        _day = day
        while len(ndays)<n:
            _day = self.previous_day(_day)
            ndays.append(_day)
        ndays.sort();
        return ndays

    def previous_n_days_str(self, day_str, day_str_format = '%Y%m%d', n=20):
        ndays = []
        day = day_str
        while len(ndays)<n:
            day = self.previous_day_str(day, day_str_format)
            ndays.append(day)
        ndays.sort();
        return ndays

    def next_n_days_str(self, day_str, day_str_format = '%Y%m%d', n=20):
        ndays = []
        day = day_str
        while len(ndays)<n:
            day = self.next_day_str(day, day_str_format)
            ndays.append(day)
        ndays.sort();
        return ndays
    
    def get_trade_days(self, start_date, end_date):
        if(start_date>end_date):
            return []
        ndays = []
        day = start_date
        while day<=end_date:
            if(self.is_trade_day(day)):
                ndays.append(day)
            day += datetime.timedelta(days=1)
        ndays.sort()
        return ndays

def get_option_expiration_day():
    nyse = TradeDate("nyse")
    str_today = datetime.datetime.strftime(datetime.date.today(), '%Y%m%d')    
    option_expire_day = nyse.get_month_option_expiration(str_today)
    return option_expire_day
    
    
def get_last_day_in_month():
    nyse = TradeDate("nyse")
    day = datetime.date.today()
    return nyse._get_last_day_in_month(datetime.datetime.strftime(day, '%Y%m%d'), day_str_format='%Y%m%d')
    
def get_weekday(td, day_str_format='%Y%m%d'):
    day = datetime.datetime.strptime(td, day_str_format)
    return datetime.datetime.weekday(day)    

if __name__ == '__main__':
    import rlipy.logger
    '''countries = ["AV", #austria
                 "BB", #belgium
                 "DC", #Denmark
                 "FH", #Finland
                 "FP", #France
                 "GA", #Greece
                 "GR", #Germany
                 "ID",#Ireland
                 "IM",#Italy
                 "IR",#Iceland
                 "LN",#England
                 "LX",#Luxembourg
                 "MV",#Malta
                 "NA",#Netherlands
                 "NO",#Norway
                 "PL",#Portugal
                 "PW",#Porland
                 "SM",#Spain
                 "SS",#Sweden
                 "SW",#Switzerland
                 ]  '''
    countries = ['US','JP','HK']
    td_dir = '/home/VERITIONFUND/rli/tmp/country/'
    weekday = pd.read_csv(td_dir+'all.qap')
    for country in countries:
        td = pd.read_csv(td_dir+country+'.qap')
        holiday = weekday[-(weekday['$Weekday'].isin(td['$TradeDate']))]
        out_file = td_dir+'holiday/'+country+'.txt'
        holiday['$Weekday'].apply(lambda x: x[6:]+x[0:2]+x[3:5]).to_csv(out_file,index=False)
        
