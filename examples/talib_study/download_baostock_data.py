import numpy as np
import talib
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt

def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

def download_data(code,begin_date,end_date):
    # 获取指定日期的指数、股票数据
    # stock_rs = bs.query_all_stock(date)
    # stock_df = stock_rs.get_data()
    data_df = pd.DataFrame()
    # for code in stock_df["code"]:
    print("Downloading :" + code)
    # k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST", "2020-01-01", date)
    k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,amount,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST", begin_date, end_date)
    data_df = data_df.append(k_rs.get_data())
    return data_df

def get_all_code_local():
    df=pd.read_excel("all_stock_detail.xlsx")
    return df['stock_num'].tolist()

bs.login()
code_list= get_all_code_local()
print(code_list)
today=todayDateStr()
if not os.path.exists(today):
    os.makedirs(today)

index=0
for elem in code_list:
    index=index+1
    try:
        df=download_data(elem,"2020-01-01",today)
        df.to_excel(today+"/"+elem+".xlsx")
    except:
        traceback.print_exc
bs.logout()
