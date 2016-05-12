import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import numpy as np


def func_1(start,end,sym,alloc,p):
    dt_start = start
    dt_end = end
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ls_symbols=sym
    
    
    n_days=len(ldt_timestamps)  
    
    
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps,ls_symbols,ls_keys)  #(dias de transaccion efectivos, simbolos a leer, data a obtener)
    d_data = dict(zip(ls_keys,ldf_data))
    
    #precios normalizados
    price_close = d_data['close'].values
    price_norm_close = price_close/price_close[0]
    
    #valor del indice en base a los precios normalizados y el peso de cada activo
    index=np.dot(price_norm_close,alloc)
    
    #rendimientos diarios del indice
    index_returns=np.zeros(n_days)
    for i in range(1,n_days):
        index_returns[i]=(index[i]/index[i-1])-1

    
    #estadisticas del indice
    avg_returns= np.mean(index_returns,axis=0)
    std_returns= np.std(index_returns, axis=0)
    acc_returns= ((index[-1])/index[0])
    sharpe_ratio= (np.sqrt(252)*avg_returns/std_returns)
    if p==1:
        #imprime las estadisticas del indice optimo
        print "Sharpe Ratio: ",sharpe_ratio
        print "Volatility (stdev of daily returns):  ",std_returns
        print "Average Daily Return:  ",avg_returns
        print "Cumulative Return:  ",acc_returns
        
        #imprimir el indice vs las stocks
        plt.clf()
        plt.plot(ldt_timestamps, index,c='#24bc00',linewidth=4)
        plt.plot(ldt_timestamps, price_norm_close, alpha=0.5,linewidth=1)
        chart_symbols= ls_symbols
        chart_symbols.insert(0,"Index")
        plt.legend(chart_symbols)
        plt.ylabel('Adjusted Close')
        plt.xlabel('Date')
        plt.show()
    return(sharpe_ratio)
    

def opt(start,end,sym):
    opt_alloc=[0,0,0,0]
    opt_sharp=0
    #itero todo los posibles valores y guardo el sharpe ratio mas alto obtenido
    for i in np.linspace(0.0, 1.0, 11):         #intervalos de .10f
        for j in np.linspace(0.0, 1.0, 11):
            for k in np.linspace(0.0, 1.0, 11):
                for l in np.linspace(0.0, 1.0, 11):
                    if i+j+k+l==1:
                        alloc=[i,j,k,l]
                        results=func_1(start,end,sym,alloc,0)
                        if results>opt_sharp:
                            opt_sharp=results
                            opt_alloc=alloc
    print opt_sharp
    print opt_alloc
    results=func_1(start,end,sym,alloc,1)
                        
    

sym=['AXP', 'HPQ', 'IBM', 'HNZ']
start = dt.datetime(2010,1,1)
end = dt.datetime(2010,12,31)
opt(start,end,sym)
