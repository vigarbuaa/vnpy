import numpy as np
import talib
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt

def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

def download_data(code,begin_date,end_date):
    data_df = pd.DataFrame()
    print("Downloading :" + code)
    k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,amount,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST", begin_date, end_date)
    data_df = data_df.append(k_rs.get_data())
    return data_df

def get_all_code_local():
    df=pd.read_excel("all_stock_detail.xlsx")
    return df['stock_num'].tolist()

bs.login()
code_list= get_all_code_local()
print(code_list)
# today=todayDateStr()
today="2020-07-07"
if not os.path.exists(today):
    os.makedirs(today)

index=0
df_all = pd.DataFrame()
for elem in code_list:
    index=index+1
    try:
        df=download_data(elem,today,today)
        print(df)
        df_all=df_all.append(df)
        print("----------")
        # print(df_all)
        # df.to_excel(today+"/"+elem+".xlsx")
    except:
        traceback.print_exc
bs.logout()
# df_all.to_excel(today+"/"+"all_code"+".xlsx")
df_all.to_excel("2020-07-08"+"/"+"all_code"+".xlsx")
