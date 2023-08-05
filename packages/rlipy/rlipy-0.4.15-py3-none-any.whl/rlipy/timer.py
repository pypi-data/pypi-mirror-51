import datetime
class Timer(object):
    def __init__(self, seconds):
        self.interval = datetime.timedelta(0, seconds)
        self.reset()
    
    def expired(self):
        now =  datetime.datetime.now();
        return now>self.expireTime
    
    def reset(self):
        now =  datetime.datetime.now();
        self.expireTime = datetime.datetime.now()+self.interval
    
    