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
  df['dif']=macd
  df['dem']=signal
  df['hist']=hist
#   print(df.tail(3))
  return df

def macd_buy_signal1(df):
  # 金叉 macd
  if(df["dif"][-1] > df["dem"][-1] and df["dif"][-2] <= df["dem"][-2]):
    return True
  else:
    return False 

def macd_buy_signal2(df):
  # 金叉 macd 
  if(df["dif"][-1] > df["dem"][-1] and df["dif"][-2] > df["dem"][-2] and df["dif"][-3]<=df["dem"][-3]):
    return True
  else:
    return False 

def macd_short_signal1(df):
  # 卖出信号1
  if(df["dif"][-1] < df["dem"][-1] and df["dif"][-2] >= df["dem"][-2]):
    return True
  else:
    return False 

def macd_short_signal2(df):
  # 卖出信号2
  if(df["dif"][-1] < df["dem"][-1] and df["dif"][-2] < df["dem"][-2] and df["dif"][-3]>=df["dem"][-3]):
    return True
  else:
    return False 

  #### 结果集输出到csv文件 ####   
  # print(result)
  
# stock_list=["sh.600276","sz.002352","sz.000596","sh.600660","sh.601009","sh.600036","sz.000651","sz.000333"]
stock_list=["sz.399006","sh.600276","sz.300033","sz.002352","sz.000596","sh.600660","sh.601009","sh.000001","sh.600036","sz.000651","sz.000333","sz.002821","sz.300347","sh.601012","sh.603195","sh.600779","sz.000858","sh.603719","sh.603882","sz.300326","sh.603259","sz.300015","sh.600585","sz.300750","sz.002594","sh.600129","sz.002142","sz.002812","sh.603087","sz.300285","sz.300529","sh.600380","sz.000001","sh.600009","sh.600519","sh.600900","sz.002410"]
# stock="sh.600585"
#### 登陆系统 ####
lg = bs.login()
# print('login respond error_code:'+lg.error_code)
# print('login respond  error_msg:'+lg.error_msg)
# 显示登陆返回信息
for stock in stock_list:
    df = get_stock_df(stock)
    # analyse df
    if(macd_buy_signal1(df)):
        print("买入信号1: " + stock)
    if(macd_buy_signal2(df)):
        print("买入信号2: " + stock)
    if(macd_short_signal1(df)):
        print("卖出信号1: " + stock)
    if(macd_short_signal2(df)):
        print("卖出信号2: " + stock)
    # send email
bs.logout()