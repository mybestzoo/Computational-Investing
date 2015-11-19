import sys
import csv
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import time
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

def marketsim( start_cash, orders_file ) :
#read csv
 orders = csv.reader(open(orders_file,'rU'),delimiter=',')
 #create two lists for all dates and symbols
 symbols = []
 dates = []
 for row in orders:
	dates.append(dt.date(int(row[0]),int(row[1]),int(row[2])))
	symbols.append(row[3])
	print(1)
 #remove duplicates
 symbols = list(set(symbols))
 dates = list(set(dates))
 #set the data provider to Yahoo
 database = da.DataAccess('Yahoo')
 #timestamps for close of every trading day ?: add +dt.timedelta(days=1)
 timestamps = du.getNYSEdays( dates[0] , dates[-1] , dt.timedelta(hours=16) )
 #read actual close price for symbols on dates
 data = database.get_data(timestamps,symbols,'actual_close')
 #create trade matrix
 trade_matrix = pd.DataFrame( 0 , index = timestamps , columns = symbols)
 #fill trade matrix with number of shares
 for row in orders:
	dates.append(dt.date(int(row[0]),int(row[1]),int(row[2])))
	symbols.append(row[3])
	print(0);
 return ;

start_cash = sys.argv[1]
orders_file  = sys.argv[2]

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
 
marketsim( start_cash, orders_file )

