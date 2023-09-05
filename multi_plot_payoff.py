
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from helpers import payoff_calculator, check_optype, check_trtype

abb={'c': 'Call',
    'p': 'Put',
    'b': 'Long',
    's': 'Short'}

def multi_plotter(spot_range, spot,
                op_list=[{'op_type':'c','strike':44500,'tr_type':'s','op_pr':182.55,'contract':15},
                {'op_type':'p','strike':44600,'tr_type':'s','op_pr':214,'contract':30}], 
                  save=False, file='fig.png'):



    spot1=(spot//100)*100

    x=np.arange(spot1-spot_range,spot1+spot_range,100)

    y0=np.zeros_like(x)         
    
    y_list=[]
    for op in op_list:
        op_type=str.lower(op['op_type'])
        tr_type=str.lower(op['tr_type'])
        check_optype(op_type)
        check_trtype(tr_type)
        
        strike=op['strike']
        op_pr=op['op_pr']
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

            y+=np.array(y_list[i])
        
        sns.lineplot(x=x, y=y, label='combined', alpha=1, color='k')
        plt.axhline(color='k', linestyle='--')
        plt.axvline(x=spot, color='r', linestyle='--', label='spot price')


        plt.legend()
        plt.legend(loc='upper right')
        title="Multiple Options Plotter"
        plt.title(title)
        plt.fill_between(x, y, 0, alpha=0.2, where=y>y0, facecolor='green', interpolate=True)
        plt.fill_between(x, y, 0, alpha=0.2, where=y<y0, facecolor='red', interpolate=True)


        plt.tight_layout()
        if save==True:
            plt.savefig(file)
        plt.show()


    plotter()      

df= pd.read_csv("/home/bps/Desktop/krishan/data scraping/payoffs/Net positions Daily 04-09-23.csv")
options_df = df[(df['Instrument Name '] == 'OPTIDX ') & (df['Symbol '] == "BANKNIFTY ")]

filtered_df = options_df[ ((options_df['Net Qty ']).notnull()) ]
filtered_df['Net Qty '] = pd.to_numeric(filtered_df['Net Qty '], errors='coerce')
filtered_df['Net_Price'] = filtered_df.apply(lambda row: row['Sell Avg. '] if row['Net Qty '] <= 0 else row['Buy Avg. '], axis=1)

filtered_df['op_type']=filtered_df.apply(lambda row: 'c' if row['Option Type '] == 'CE ' else 'p', axis=1)
filtered_df['tr_type']=filtered_df.apply(lambda row: 's' if row['Net Qty '] <=0  else 'b', axis=1)
spot=float(filtered_df['Spot Price'].iloc[1])
filtered_df = filtered_df[['op_type','Strike Price ','tr_type','Net_Price',  'Net Qty '  ]]

print("spot", spot)
selected_columns_df = filtered_df[pd.to_numeric(filtered_df['Net Qty '], errors='coerce').notnull()]
selected_columns_df.loc[:, 'Net Qty '] = abs(selected_columns_df['Net Qty '])
two_d_list = selected_columns_df.values.tolist()

list_dict=[]
for item in two_d_list:
    temp = {
        'op_type': item[0],
        'strike': float((item[1])),
        'tr_type': item[2],
        'op_pr': float(item[3]),
        'contract': item[4]
    }
    list_dict.append(temp)

print(list_dict)

spot_range=3000
print(list_dict)
multi_plotter(spot_range,spot, list_dict)

