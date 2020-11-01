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
  ma5 = talib.SMA(df.close,5)
  ma10 = talib.SMA(df.close,10)
  ma20 = talib.SMA(df.close,20)
  df['ma5']=ma5
  df['ma10']=ma10
  df['ma20']=ma20
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

def short_ma5(df):
  return True if(df["close"][-1]<df["ma5"][-1]) else False

def short_ma10(df):
  return True if(df["close"][-1]<df["ma10"][-1]) else False

def short_ma20(df):
  return True if(df["close"][-1]<df["ma20"][-1]) else False

  #### 结果集输出到csv文件 ####   
  # print(result)
  
# stock_list=["sh.600276","sz.002352","sz.000596","sh.600660","sh.601009","sh.600036","sz.000651","sz.000333"]
# stock_list=["sz.399006","sh.600276","sz.300033","sz.002352","sz.000596","sh.600660","sh.601009","sh.000001","sh.600036","sz.000651","sz.000333","sz.002821","sz.300347","sh.601012","sh.603195","sh.600779","sz.000858","sh.603719","sh.603882","sz.300326","sh.603259","sz.300015","sh.600585","sz.300750","sz.002594","sh.600129","sz.002142","sz.002812","sh.603087","sz.300285","sz.300529","sh.600380","sz.000001","sh.600009","sh.600519","sh.600900","sz.002410"]
stock_list=["sh.600066","sz.000002","sz.002415","sh.600031","sz.399006","sh.600276","sz.300033","sz.002352","sz.000596","sh.600660","sh.601009","sh.000001","sh.600036","sz.000651","sz.000333","sz.002821","sz.300347","sh.601012","sh.603195","sh.600779","sz.000858","sh.603719","sh.603882","sz.300326","sh.603259","sz.300015","sh.600585","sz.300750","sz.002594","sh.600129","sz.002142","sz.002812","sh.603087","sz.300285","sz.300529","sh.600380","sz.000001","sh.600009","sh.600519","sh.600900","sz.002410","sh.601318","sh.601336","sz.002475"]
# stock="sh.600585"
#### 登陆系统 ####
lg = bs.login()
# print('login respond error_code:'+lg.error_code)
# print('login respond  error_msg:'+lg.error_msg)
# 显示登陆返回信息
buy_list1=[]
buy_list2=[]
sell_list1=[]
sell_list2=[]
short_ma5_list=[]
short_ma10_list=[]
short_ma20_list=[]
for stock in stock_list:
    df = get_stock_df(stock)
    # analyse df
    if(macd_buy_signal1(df)):
        print("买入信号1: " + stock)
        buy_list1.append(stock)
    if(macd_buy_signal2(df)):
        print("买入信号2: " + stock)
        buy_list2.append(stock)
    if(macd_short_signal1(df)):
        print("卖出信号1[macd]: " + stock)
        sell_list1.append(stock)
    if(macd_short_signal2(df)):
        print("卖出信号2[macd]: " + stock)
        sell_list2.append(stock)
    if(short_ma5(df)):
        print("跌破ma5: " + stock)
        short_ma5_list.append(stock)
    if(short_ma10(df)):
        print("跌破ma10: " + stock)
        short_ma10_list.append(stock)
    if(short_ma20(df)):
        print("跌破ma20,及时止损: " + stock)
        short_ma20_list.append(stock)
    # send email
bs.logout()
print("买入1: "+buy_list1)
print("买入2: "+buy_list2)
print("卖出1: "+sell_list1)
print("卖出2: " +sell_list2)
print("跌破5日线: "+short_ma5_list)
print("跌破10日线："+short_ma10_list)
print("破破20日线："+short_ma20_list)