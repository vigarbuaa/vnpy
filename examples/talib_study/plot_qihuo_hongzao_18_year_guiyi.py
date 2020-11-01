# encoding: UTF-8
from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, time, json, sys, traceback, logging, getopt
import talib
import tushare as ts
import copy

#--------------------------------------------------------------------------------
def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

#--------------------tushare api-------------------------------------------------
ts.set_token("254380d6aca11ec05e075e58dfe175a0c6f5d8b3d727431b248d70cf")
pro = ts.pro_api()

def convert_df_date(df):
    df['date']=pd.to_datetime(df['trade_date'])
    df.set_index('date',inplace=True)
    df_ret = df.drop(columns=['trade_date'])
    return df_ret

def get_fut_info(symbol, zero_df):
    df_raw = pro.fut_daily(ts_code=symbol, start_date='20180101',fields='trade_date,close')
    df = convert_df_date(df_raw)
    df_ret= df+ zero_df
    return df_ret

df_all = pd.read_excel("all_comp_info.xlsx")
def get_symbol_name(symbol,df_all):
    return df_all[df_all['ts_code']==symbol].name

def merge_df(df1,df2):
    df1['dapan']=df2['close']
    df1 = (df1-df1.min())/(df1.max()-df1.min())
    return df1

df_sz_raw = pro.fut_daily(ts_code='JDL.DCE',start_date="20180101",fields='trade_date,close')
df_sz = convert_df_date(df_sz_raw)

df_zero= copy.copy(df_sz)
df_zero['close']=0
# 南京银行
# df_ret.plot()
symbol_list = ["JD2005.DCE","JD2006.DCE","JD2007.DCE","JD2008.DCE","JD2009.DCE","JD2010.DCE","JD2011.DCE","JD2012.DCE","JD2101.DCE","JD2102.DCE","JD2103.DCE"]
# symbol_list = ["CJ2005.DCE","CJ2007.DCE","CJ2009.DCE","CJ2012.DCE","CJ2101.DCE","CJ2103.DCE"]

length= len(symbol_list)
fig,axes = plt.subplots(length+1,1,figsize=(15,length*8))

# 头里先画主力
axes[0].set_title("主力指数",fontproperties='SimHei', fontsize=15)
df_sz.plot(ax=axes[0])

index=0

for elem in symbol_list:
    symbol = elem
    print(symbol)
    index=index+1
    df = get_fut_info(symbol, df_zero)
    #name = get_symbol_name( symbol, df_all )
    #axes[index].set_title(symbol+"--"+name.iloc[0],fontproperties='SimHei', fontsize=15)
    axes[index].set_title(symbol,fontproperties='SimHei', fontsize=15)
    df_plot = merge_df(df,df_sz)
    df_plot.plot(ax=axes[index])

pic_name="test_jd_411.v1.png"
png_output_dir=".\\analyse_png\\"
plt.subplots_adjust(hspace=0.5)
plt.savefig(png_output_dir+pic_name)
