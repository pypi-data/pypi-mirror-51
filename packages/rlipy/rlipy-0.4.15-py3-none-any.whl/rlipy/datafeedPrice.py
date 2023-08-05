class Price():

    def __init__(self):
        self.symbol = ''
        self.bidPrice = ''
        self.bidSpread = ''
        self.benchmark = ''
        self.askPrice = ''
        self.askSpread = ''
        self.benchmark = ''
        self.time = ''
        self.flags = ''

    def invalidatePrice(self):
        self.bidPrice = ''
        self.bidSpread = ''
        self.benchmark = ''
        self.askPrice = ''
        self.askSpread = ''
        self.benchmark = ''
        return self

    def __str__(self):
        # 4 stand of IDSource ISIN
        return  '%s|%s|%s|%s|4|%s|%s|%s|4|%s|%s' % (self.symbol,
             self.bidPrice, self.bidSpread, self.benchmark,
             self.askPrice, self.askSpread, self.benchmark,
             self.time,
             self.flags
             )

    def merge(self, other):
        for k, v in list(other.__dict__.items()):
            self.__setattr__(k, v)

    def __eq__(self, other):
        if(other == None): return False
        return self.__dict__ == other.__dict__
