import numpy as np
import talib
import os, time, json, sys, traceback, logging, getopt
import baostock as bs
import pandas as pd

def get_stock_df(stock_num):
  # rs = bs.query_history_k_data_plus(stock,"date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
  rs = bs.query_history_k_data_plus(stock,"date,code,open,high,low,close,volume,amount",
      start_date='2019-01-01', end_date='2020-10-31',
      frequency="d", adjustflag="3")
  print('query_history_k_data_plus respond error_code:'+rs.error_code)
  print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
  
  #### 打印结果集 ####
  data_list = []
  while (rs.error_code == '0') & rs.next():
      # 获取一条记录，将记录合并在一起
      data_list.append(rs.get_row_data())
  result = pd.DataFrame(data_list, columns=rs.fields)
  result.to_csv(stock+"_k_data.csv", index=False)
  df = pd.read_csv(stock+"_k_data.csv",header=0,index_col=0)
#   print(df.tail(3))
  
  macd, signal, hist = talib.MACD(df.close,fastperiod=12,slowperiod=26,signalperiod=9)
  df['macd']=macd
  df['signal']=signal
  df['hist']=hist
  print(df.tail(3))
  return df
  
  #### 结果集输出到csv文件 ####   
  # print(result)
  
stock_list=["sh.600585","sh.600009"]
# stock="sh.600585"
#### 登陆系统 ####
lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)
# 显示登陆返回信息
for stock in stock_list:
    df = get_stock_df(stock)
    # analyse df

    # send email
bs.logout()