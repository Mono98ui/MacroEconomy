import backtrader as bt
#
# This class represent the bell sell strategy.
#
class IndicatorStrat(bt.Strategy):

    def __init__(self):
        self.threemonthyield = self.datas[0].close
        self.indicator = self.datas[1].close

    def next(self):
        if not self.position:  # not in the market
            if self.indicator >= 0.5:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.indicator < 0.5:  # in the market & cross to the downside
            self.close()