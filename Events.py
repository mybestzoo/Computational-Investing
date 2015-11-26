import operator
import csv
import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the csv file with orders:
When an event occurs, buy 100 shares of the equity on that day.
Sell automatically 5 trading days later.
"""

def sortcsv(csvfilename, themanyfieldscolumnnumbers):
	data = csv.reader(open(csvfilename),delimiter=',')
	sortedlist = sorted(data, key=operator.itemgetter(*themanyfieldscolumnnumbers))    # 0 specifies according to first column we want to sort
    #now write the sorte result into new CSV file
	with open("NewFile.csv", "wb") as f:
		fileWriter = csv.writer(f, delimiter=',')
		for row in sortedlist:
			fileWriter.writerow(row)


def sortcsv1(csvfilename, themanyfieldscolumnnumbers):
  with open(csvfilename, 'rb') as f:
    readit = csv.reader(f)
    thedata = list(readit)
  thedata.sort(key=operator.itemgetter(*themanyfieldscolumnnumbers))
  with open(csvfilename, 'wb') as f:
    writeit = csv.writer(f)
    writeit.writerows(thedata)

def find_events(ls_symbols, d_data):
	''' Finding the event dataframe '''
	df_close = d_data['actual_close']
	#ts_market = df_close['SPY']

	print "Finding Events"

	# Creating an empty dataframe
	df_events = copy.deepcopy(df_close)
	df_events = df_events * np.NAN

	# Time stamps for the event range
	ldt_timestamps = df_close.index
	
	# create csv file for trade orders
	writer = csv.writer(open('TradeOrders.csv','wb'), delimiter=',')	

	for s_sym in ls_symbols:
		for i in range(1, len(ldt_timestamps)):
			f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
			f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
			# Event is found if the symbol goes less than 5 while the previous day t was more than 5
			if f_symprice_today < 5.0 and f_symprice_yest >= 5.0:
				buy_row = [ldt_timestamps[i] , s_sym, 'BUY', 100]
				sell_row = [ldt_timestamps[i+5] , s_sym, 'SELL', 100]
				writer.writerow(buy_row)
				writer.writerow(sell_row)
	
	# sort csv by date
	sortcsv('TradeOrders.csv',[0])
		
		
	return df_events


if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data)
    print "Creating trade orders"
