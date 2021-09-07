import pandas as pd
import pandas_datareader as pdr
import datetime
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#
#This class communicate with the app and the csv file where data are stock.
#
class DataManager:
    
    
    def __init__(self, start, end):

        self.CONST_FRED = 'fred'
    
        self.labeldict = {
            "MYAGM1USM052S": "M1 Money Stock",
            "MYAGM2USM052S": "M2 Money Stock",
            "BOGZ1FL893169105Q":"All Sectors; Commercial Paper; Liability",
            "BUSLOANS": " Commercial and Industrial Loans",
            "TOTALSL": "Total Consumer Credit Owned and Securitized, Outstanding",
            "INDPRO": "Industrial Production: Total Index",
            "NOCDFSA066MSFRBPHI": "Current New Orders; Diffusion Index for Federal Reserve District 3: Philadelphia ",
            "PCE": "Personal Consumption Expenditures",
            "PAYEMS": "All Employees, Total Nonfarm",
            "AWHMAN": "Average Weekly Hours of Production and Nonsupervisory Employees, Manufacturing",
            "USALOLITONOSTSAM": "Leading Indicators OECD: Leading indicators: CLI: Normalised for the United States",
            "HOUST": "New Privately-Owned Housing Units Started: Total Units",
            "PERMIT": "New Privately-Owned Housing Units Authorized in Permit-Issuing Places: Total Units",
            "RETAIL": "Retail Sales (Monthly)",
            "IC4WSA": "4-Week Moving Average of Initial Claims",
            "HTRUCKSSA": "Motor Vehicle Retail Sales: Heavy Weight Trucks",
            "BOGZ1FL145020011Q": "Nonfinancial Business; Inventories (Excluding Farms)",
            "CPIAUCSL": "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average",
            "PPIACO": "Producer Price Index by Commodity: All Commodities",
            "AHETPI": "Average Hourly Earnings of Production and Nonsupervisory Employees, Total Private",
            "DTWEXM": "Trade Weighted U.S. Dollar Index: Major Currencies, Goods",
            "NFORBRES": "Net Free or Borrowed Reserves of Depository Institutions",
            "BOGNONBR": "Non-Borrowed Reserves of Depository Institutions",
            "REQRESNS": "Required Reserves of Depository Institution",
            "T10YFF": "10-Year Treasury Constant Maturity Minus Federal Funds Rate",
            "DTB3": "3-Month Treasury Bill: Secondary Market Rate",
            "FEDFUNDS": "Effective Federal Funds Rate",
            "INTDSRUSM193N": "Interest Rates, Discount Rate for United States",
            "GACDFSA066MSFRBPHI": " Current General Activity; Diffusion Index for Federal Reserve District 3: Philadelphia",
            "TB3MS":"3-Month Treasury Bill: Secondary Market Rate (1934)",
        }
    
        self.dfdict = {}
          
        self.start = start
        self.end = end
        
        self._update()
            
    
    #key = id
    def showplots(self, listKeys):
        
        for key in listKeys:
            df = pd.read_csv('Data/{key}.csv'.format(key=key))
            fig = px.line(df, y = key ,
                  title="{title} {yearStart}-{yearEnd}".format(title=self.labeldict[key], yearStart=self.start.year, 
                                                                   yearEnd=self.end.year),
                  labels={key :self.labeldict[key]})
            fig.show()
        
    
    def displayDF(self, listKeys):
        for key in listKeys:
            display(pd.read_csv('Data/{key}.csv'.format(key=key)))
            
            
    # def showplotAll(self):
    #     for key, value in self.labeldict.items():
    #         fig = px.line(self.dfdict[key], y = key ,
    #               title="{title} {yearStart}-{yearEnd}".format(title=value, yearStart=self.start.year, 
    #                                                                yearEnd=self.end.year))
    #         fig.show()
            
    # def displayDFAll(self):
    #     for value in self.dfdict.itervalues():
    #         display(value)    
    
    def getlabeldict(self):
        return self.labeldict
    
    def getmoneycreditgrowth(self):
        return {
            "MYAGM1USM052S": "M1 Money Stock",
            "MYAGM2USM052S": "M2 Money Stock",
            "BOGZ1FL893169105Q":"All Sectors; Commercial Paper; Liability",
            "BUSLOANS": " Commercial and Industrial Loans",
            "TOTALSL": "Total Consumer Credit Owned and Securitized, Outstanding"}

    def getdfdict(self):
        return self.dfdict
    
    def getstartdate(self):
        return self.start
    
    def getenddate(self):
        return self.end
    
    def setstartdate(self, newStart):
        self.start = newStart
        self._update()
        self.create_csv()
        
    def setenddate(self, newEnd):
        self.end = newEnd
        self._update() 
        self.create_csv()
    
    def _update(self):
        for key in self.labeldict:
            self.dfdict[key] = pdr.DataReader(key, self.CONST_FRED, self.start, self.end)
            self.dfdict[key].dropna(inplace=True)
    
    def create_csv(self):
        for key, value in self.dfdict.items():
            value.to_csv('Data/{key}.csv'.format(key=key))

    def addcolumn_csv(self, listKeys,columnName, results):
        for key in listKeys:
            df = pd.read_csv('Data/{key}.csv'.format(key=key),index_col=0)
            df[columnName] = results[key]
            df.to_csv('Data/{key}.csv'.format(key=key))
    