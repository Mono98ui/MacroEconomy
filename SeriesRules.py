import pandas as pd
import pandas_datareader as pdr
import datetime
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#
#This class used the data on the csv and compute three month grwoth and twelve month growth
#
class SeriesRules:

    def __init__(self,dfkeys):
        self.dfkeys = dfkeys
    
    def createthreemonthrule(self):

        results = {}

        for key in self.dfkeys:
            df = pd.read_csv('Data/{key}.csv'.format(key=key))
            first = datetime.datetime.strptime(df["DATE"][0], '%Y-%m-%d')
            second = datetime.datetime.strptime(df["DATE"][1], '%Y-%m-%d')

            diff = second - first

            results[key] = self._computethreemonth(key, df, diff)
        
        return results

    def _computethreemonth(self, key, df, diff):

        results = []
        idIndex = 0

        for i in range(df.shape[0]):

            #day = indice 90/0
            if diff.days == 1 and i-90 >= 0:
                idIndex = 0
                growth = (((df[key][i]/df[key][i-90])**(12/3))-1)*100
                results.append(growth)
                #print(growth)

            #week = indice 12/0
            elif diff.days <= 7 and diff.days >=5 and i-12 >= 0:
                idIndex = 1
                growth = (((df[key][i]/df[key][i-12])**(12/3))-1)*100
                results.append(growth)
                #print(growth)

            #month = indice 3/0
            elif diff.days > 28 and diff.days < 32 and i-3 >= 0:
                idIndex = 2
                growth = (((df[key][i] /df[key][i-3])**(12/3))-1)*100
                results.append(growth)
                #print(growth)

            #3 month = indice 1/0   
            elif diff.days >= 32 and i-1 >= 0:
                idIndex = 3
                growth = (((df[key][i] /df[key][i-1])**(12/3))-1)*100
                results.append(growth)
                #print(growth)
            
        if idIndex == 0:
            self._formatrule(90, results)
        elif idIndex == 1:
            self._formatrule(12, results)
        elif idIndex == 2:
            self._formatrule(3, results)
        else:
            self._formatrule(1, results)

        return results

    def createtwelvemonthrule(self):

        results = {}

        for key in self.dfkeys:
            df = pd.read_csv('Data/{key}.csv'.format(key=key))
            first = datetime.datetime.strptime(df["DATE"][0], '%Y-%m-%d')
            second = datetime.datetime.strptime(df["DATE"][1], '%Y-%m-%d')

            diff = second - first

            results[key] = self._computetwelvemonth(key, df, diff)

        return results

    def _computetwelvemonth(self, key, df, diff):

        results = []
        idIndex = 0

        for i in range(df.shape[0]):

            #day = indice 261/0
            if diff.days == 1 and i-261 >= 0:
                idIndex = 0
                growth = (((df[key][i]/df[key][i-261])**(12/12))-1)*100
                results.append(growth)
                #print(growth)

            #week = indice 52/0
            elif diff.days <= 7 and diff.days >=5 and i-52 >= 0:
                idIndex = 1
                growth = (((df[key][i]/df[key][i-52])**(12/12))-1)*100
                results.append(growth)
                #print(growth)

            #month = indice 12/0
            elif diff.days > 28 and diff.days < 32 and i-12 >= 0:
                idIndex = 2
                growth = (((df[key][i] /df[key][i-12])**(12/12))-1)*100
                results.append(growth)
                #print(growth)

            #3 month = indice 4/0
            elif diff.days >= 32 and i-4 >= 0:
                idIndex = 3
                growth = (((df[key][i] /df[key][i-4])**(12/12))-1)*100
                results.append(growth)
                #print(growth)
        
        if idIndex == 0:
            self._formatrule(261, results)
        elif idIndex == 1:
            self._formatrule(52, results)
        elif idIndex == 2:
            self._formatrule(12, results)
        else:
            self._formatrule(4, results)

        return results

    def _formatrule(self, nbr, results):
        for i in range(nbr):
            results.insert(i, None)