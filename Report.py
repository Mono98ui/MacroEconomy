import pandas as pd
import datetime
import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.analyzers as btanalyzers
from ThreeTwelveCross import ThreeTwelveCross
from YoyGrowth import YoyGrowth
#
# This class visualise the strategy and create a report base on the strategy.
#
class Report:

    def __init__(self):
        self.tbthree = "Data/TB3MS.csv"
        self.start = datetime.datetime(1985, 1, 4)
        self.end = datetime.datetime(2010, 1, 4)
        self.dateFormat = "%Y-%m-%d"
        self.threeColumn = 2
        self.twelveColumn = 3
        self.timeframe = bt.TimeFrame.Months
        self.dictDf = {}
        self.listNames = ["title","total","win-count",
        "percent-win","pnl-average", "trade-len","expected-value"]


    def generateStratChart(self, key, value):
        cerebro = bt.Cerebro()

        cerebro = bt.Cerebro(stdstats=False)  # remove the standard observers
        cerebro.addobserver(bt.observers.Trades)

        cerebro.addobserver(
                bt.observers.BuySell,
                barplot=True,
                bardist=0.015)

        cerebro.addstrategy(ThreeTwelveCross)

        data1 = btfeeds.GenericCSVData(
            dataname=self.tbthree,

            fromdate=self.start,
            todate=self.end,
            timeframe=self.timeframe ,
            nullvalue=0.0,

            dtformat=(self.dateFormat),

            datetime=0,
            high=1,
            low=1,
            open=1,
            close=1,
            volume=-1,
            openinterest=-1
        ) 
        cerebro.adddata(data1, name='3-month-yield')

        data2 = btfeeds.GenericCSVData(
            dataname="Data/{name}.csv".format(name=key),

            fromdate=self.start,
            todate=self.end,
            timeframe=self.timeframe ,
            nullvalue=0.0,

            dtformat=(self.dateFormat),

            datetime=0,
            high=self.threeColumn,
            low=self.threeColumn ,
            open=self.threeColumn ,
            close=self.threeColumn ,
            volume=-1,
            openinterest=-1
        ) 

        cerebro.adddata(data2, name="{val} 3-month growth".format(val=value))

        data3 = btfeeds.GenericCSVData(
            dataname="Data/{name}.csv".format(name=key),

            fromdate=self.start,
            todate=self.end,
            timeframe=self.timeframe ,
            nullvalue=0.0,

            dtformat=(self.dateFormat),

            datetime=0,
            high=self.twelveColumn,
            low=self.twelveColumn,
            open=self.twelveColumn,
            close=self.twelveColumn,
            volume=-1,
            openinterest=-1
        )

        data3.compensate(data2)  # let the system know ops on data1 affect data0
        data3.plotinfo.plotmaster = data2
        data3.plotinfo.sameaxis = True

        cerebro.adddata(data3, name='{val} 12 month growth'.format(val=value))
        cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='tradeanalyzer')

        thestrats = cerebro.run()
        thestrat = thestrats[0]

        cerebro.plot()

        result =  thestrat.analyzers.tradeanalyzer.get_analysis()
        
        return result

    def generateStratChartYoyGrowth(self, key, value):
        cerebro = bt.Cerebro()

        cerebro = bt.Cerebro(stdstats=False)  # remove the standard observers
        cerebro.addobserver(bt.observers.Trades)

        cerebro.addobserver(
            bt.observers.BuySell,
            barplot=True,
            bardist=0.015)

        cerebro.addstrategy(YoyGrowth)

        data1 = btfeeds.GenericCSVData(
            dataname=self.tbthree,

            fromdate=self.start,
            todate=self.end,
            timeframe=self.timeframe,
            nullvalue=0.0,

            dtformat=(self.dateFormat),

            datetime=0,
            high=1,
            low=1,
            open=1,
            close=1,
            volume=-1,
            openinterest=-1
        )
        cerebro.adddata(data1, name='3-month-yield')

        data2 = btfeeds.GenericCSVData(
            dataname="Data/{name}.csv".format(name=key),

            fromdate=self.start,
            todate=self.end,
            timeframe=self.timeframe,
            nullvalue=0.0,

            dtformat=(self.dateFormat),

            datetime=0,
            high=self.twelveColumn,
            low=self.twelveColumn,
            open=self.twelveColumn,
            close=self.twelveColumn,
            volume=-1,
            openinterest=-1
        )

        cerebro.adddata(data2, name='{val} 12 month growth'.format(val=value))
        cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='tradeanalyzer')

        thestrats = cerebro.run()
        thestrat = thestrats[0]

        cerebro.plot()

        result = thestrat.analyzers.tradeanalyzer.get_analysis()

        return result
    
    def createCsvReport(self, result, key, value):

        self.dictDf[self.listNames[0]] = "buy 3 month/ 12 month {name}".format(name=value)
        self.dictDf[self.listNames[1]] = result.total.total
        self.dictDf[self.listNames[2]] = result.won.total
        self.dictDf[self.listNames[3]] = float(self.dictDf["win-count"])/float(self.dictDf["total"])
        self.dictDf[self.listNames[4]] = result.pnl.gross.average
        self.dictDf[self.listNames[5]] = result.len.average
        self.dictDf[self.listNames[6]] = self.dictDf[self.listNames[3]] * self.dictDf[self.listNames[4]]
        df = pd.DataFrame(self.dictDf.items(), columns=["label","value"])
        #title
        print(df.loc[ 0 , : ]["value"])
        display(df)
        df.to_csv("DataReport/{name}.csv".format(name=key))
        
    def createCsvReportYoyGrowth(self, result, key, value):

        self.dictDf[self.listNames[0]] = "buy 12 month YoY {name}".format(name=value)
        self.dictDf[self.listNames[1]] = result.total.total
        self.dictDf[self.listNames[2]] = result.won.total
        self.dictDf[self.listNames[3]] = float(self.dictDf["win-count"])/float(self.dictDf["total"])
        self.dictDf[self.listNames[4]] = result.pnl.gross.average
        self.dictDf[self.listNames[5]] = result.len.average
        self.dictDf[self.listNames[6]] = self.dictDf[self.listNames[3]] * self.dictDf[self.listNames[4]]
        df = pd.DataFrame(self.dictDf.items(), columns=["label","value"])
        #title
        print(df.loc[ 0 , : ]["value"])
        display(df)
        df.to_csv("DataReport/{name}.csv".format(name=key))