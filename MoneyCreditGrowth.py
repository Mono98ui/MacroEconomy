import pandas as pd
#
#This class compute the average: sum i + sum i -1 divided by 5 which represent the indicator. 
#
class MoneyCreditGrowth:

    def __init__(self):
        pass

    def computeSumIndex(self):
        tabSum = []
        tabAv = []
        df = pd.read_csv("DataReport/results-MoneyCredit.csv", index_col=0)
        for i in range(len(df.index)):
            sum = 0
            for j in range(5):     
                sum+=df.iloc[i][j+1]
            
            if len(tabSum)> 1:
                sum+= tabSum[i - 1]
            
            tabSum.append(sum)
            tabAv.append(sum/5)
        
        df["sum"] = tabSum
        df["average"] = tabAv
        
        df.to_csv("DataReport/results-MoneyCredit.csv")
