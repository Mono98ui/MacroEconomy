import backtrader as bt
#
#This class represent the Year over year growth. 
#
class YoyGrowth(bt.Strategy):


    def __init__(self):
        self.threemonthyield = self.datas[0].close
        #self.threemonth = self.datas[1].close  # 3m growth rate
        self.twelvemonth = self.datas[1].close  # 12m growth rate
        #self.crossover = bt.ind.CrossOver(self.threemonth, self.twelvemonth)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.twelvemonth > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.twelvemonth < 0:  # in the market & cross to the downside
            self.close()  # close long position