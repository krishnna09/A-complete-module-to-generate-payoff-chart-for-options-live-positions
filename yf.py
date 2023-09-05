import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

from helpers import check_ticker, check_optype, check_trtype, payoff_calculator

import warnings
warnings.filterwarnings('ignore')

abb={'c': 'Call',
    'p': 'Put',
    'b': 'Long',
    's': 'Short'}

def yf_plotter(ticker='msft',exp='default',spot_range=10,
               op_list=[{'op_type':'c','strike':300,'tr_type':'b', 'contract':1},
                        {'op_type':'p','strike':280,'tr_type':'b', 'contract':1}], 
                        save=False, file='fig.png'):
    
    spot=check_ticker(ticker)
    #Expiry dates
    exp_list=yf.Ticker(ticker).options
    
    x=spot*np.arange(100-spot_range,101+spot_range,0.01)/100
    y0=np.zeros_like(x)

    
    def check_exp(exp):

        if exp not in exp_list:
            raise ValueError('Option for the given date not available!')
    
    if exp=='default':
        exp=yf.Ticker('msft').options[0]
    else:
        check_exp(exp)
               
    def check_strike(df, strike):
        if strike not in df.strike.unique():
            raise ValueError('Option for the given Strike Price not available!')
    
    y_list=[]
    
    for op in op_list:
        op_type=str.lower(op['op_type'])
        tr_type=str.lower(op['tr_type'])
        
        check_optype(op_type)
        check_trtype(tr_type)
    
        if(op_type=='p'):
            df=yf.Ticker(ticker).option_chain(exp).puts
        else:
            df=yf.Ticker(ticker).option_chain(exp).calls
    
        strike=op['strike']
        check_strike(df, strike)
        op_pr=df[df.strike==strike].lastPrice.sum()
        try:
            contract=op['contract']
        except:
            contract=1
        
        y_list.append(payoff_calculator(x, op_type, strike, op_pr, tr_type, contract))
    

    def plotter():
        y=0
        plt.figure(figsize=(10,6))
        for i in range (len(op_list)):
            try:
                contract=str(op_list[i]['contract'])  
            except:
                contract='1'
                
            label=contract+' '+str(abb[op_list[i]['tr_type']])+' '+str(abb[op_list[i]['op_type']])+' ST: '+str(op_list[i]['strike'])
            sns.lineplot(x=x, y=y_list[i], label=label, alpha=0.5)
            y+=np.array(y_list[i])
        
        sns.lineplot(x=x, y=y, label='combined', alpha=1, color='k')
        plt.axhline(color='k', linestyle='--')
        plt.axvline(x=spot, color='r', linestyle='--', label='spot price')
        plt.legend()
        plt.legend(loc='upper right')
        title="OPTION STRATEGY ("+str.upper(ticker)+') '+' Exp :'+str(exp)
        plt.fill_between(x, y, 0, alpha=0.2, where=y>y0, facecolor='green', interpolate=True)
        plt.fill_between(x, y, 0, alpha=0.2, where=y<y0, facecolor='red', interpolate=True)
        plt.title(title)
        plt.tight_layout()
        if save==True:
            plt.savefig(file)
        plt.show()

    plotter()           