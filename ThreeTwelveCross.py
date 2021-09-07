import backtrader as bt
import pandas as pd
import os
import re
#
# This class represent the strategy three twelve cross using the three month interval and the twelve month. 
#
class ThreeTwelveCross(bt.Strategy):


    def __init__(self):
        self.listTrades = []
        self.listDates = []
        self.dataName = re.search("^Data\/(\w+)\.csv$", self.datas[1]._dataname).group(1)
        # mettre les autres module
        self.pathName = "DataReport/results-{name}.csv".format(name="MoneyCredit")

        self.threemonthyield = self.datas[0].close
        self.threemonth = self.datas[1].close  # 3m growth rate
        self.twelvemonth = self.datas[2].close  # 12m growth rate
        self.crossover = bt.ind.CrossOver(self.threemonth, self.twelvemonth)  # crossover signal

    def next(self):
        self.listDates.append(self.datas[0].datetime.date(0))
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long
                self.listTrades.append(1)
            else:
                self.listTrades.append(0)

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
            self.listTrades.append(-1)
        else:
            self.listTrades.append(0)
    
    def stop(self):
        serieTrades = pd.Series(self.listTrades)
        serieDates = pd.Series(self.listDates)

        dfTrades = pd.DataFrame(serieTrades)
        dfTrades = dfTrades.rename(columns = {0:"Buy/Sell {serieName}".format(serieName=self.dataName)})
        
        dfDates = pd.DataFrame(serieDates)
        dfDates = dfDates.rename(columns = {0:"Time"})

        if not os.path.isfile(self.pathName):
            df = pd.concat([dfDates,dfTrades], axis=1)
        else:
            df = pd.read_csv(self.pathName, index_col=0)

            #Remplir les donnee manquante par des dummys
            if(len(df.index) != len(self.listTrades)):
                nbrDataMissing = len(df.index)- len(self.listTrades)

                for i in range(nbrDataMissing):
                    self.listTrades.append(0)

            df["Buy/Sell {serieName}".format(serieName=self.dataName)] = self.listTrades
            #df = pd.concat([df,dfTrades], axis=1)

        df.to_csv(self.pathName) 