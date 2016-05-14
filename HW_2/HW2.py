'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep



def find_events(ls_symbols, d_data,time_study):
    ''' Finding the event dataframe '''
    df_close = d_data['close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)     
    df_events = df_events * np.NAN          #creamos una matriz con NAN en todas las casillas para todas las stocks para todas las fechas

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:            #
        for i in range(1, time_study):
            # determino el precio de los dias i, i-1
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            
            #considero como eventos todos aquellos dias en que: el dia anterior la stock tenia precio superior
            #a los $5 y en el close de este dia la accion bajo de $5
            if f_symprice_today<5 and f_symprice_yest>=5:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events


if __name__ == '__main__':
    
    
    
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2011, 1, 1)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    time_study=502  #days of the events study       /502 for 2 years/ 251 for one year/
    
    #definimos parametros y accedemos a la data
    dataobj = da.DataAccess('Yahoo')        
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')    
    ls_symbols.append('SPY')        
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']  
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)   
    
    #modifico la data a un dictado
    d_data = dict(zip(ls_keys, ldf_data))   

    
    # llenamos NaN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data,time_study)

    
    
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=120,
                s_filename='BREAK5USDPRICE_SPXOF2012_FOR20082009_returns_relativetomarket.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
