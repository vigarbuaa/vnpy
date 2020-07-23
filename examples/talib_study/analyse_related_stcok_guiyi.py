# encoding: UTF-8
import numpy as np
import talib,json
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt
from urllib import request
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import copy

#----------------------------------------------------------------------
def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

def get_all_code_local():
    df=pd.read_excel("all_stock_detail.xlsx")
    return df['stock_num'].tolist()

def get_df_from_local(code):
    symbol=code.replace(".","-")
    # target_url="http://localhost:8088/api/stockHis/"+symbol
    target_url="http://todo:8777/api/stockHis/"+symbol
    print(target_url)
    head={}
    head['User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
    target_req = request.Request(url = target_url, headers = head)
    target_response = request.urlopen(target_req)
    target_html = target_response.read().decode('utf8','ignore')
    json_raw = target_html
    json_body = json.loads(json.loads(json_raw))
    df = pd.DataFrame(json_body)
    ret = df
    ret['date_str']=pd.to_datetime(ret['date'])
    ret.set_index("date_str",inplace=True)
    ret = df.drop(columns=['ID',"date"])
    return ret 

def convert_df_date(df):
    df['date']=pd.to_datetime(df['trade_date'])
    df.set_index('date',inplace=True)
    df_ret = df.drop(columns=['trade_date'])
    return df_ret

df_all = pd.read_excel("all_comp_info.xlsx")

def merge_df(df1,df2):
    df1['dapan']=df2['close']
    df1 = (df1-df1.min())/(df1.max()-df1.min())
    return df1

# df_sz_raw = pro.fut_daily(ts_code='JDL.DCE',start_date="20180101",fields='trade_date,close')
# df_sz = convert_df_date(df_sz_raw)

# df_zero= copy.copy(df_sz)
# df_zero['close']=0
symbol_list = ["sh.688086","sz.300821","sz.000001"]

length= len(symbol_list)
# fig,axes = plt.subplots(length,1,figsize=(15,length*8))

# 头里先画主力
# axes[0].set_title("对比",fontproperties='SimHei', fontsize=15)
# df_sz.plot(ax=axes[0])

index=0

df_all = pd.DataFrame()
for elem in symbol_list:
    symbol = elem
    print(symbol)
    df = get_df_from_local(symbol)
    print(df.head(5))
    # df1 = (df1-df1.min())/(df1.max()-df1.min())
    df_all[symbol]=(df['close']-df['low'].min())/(df['high'].max()-df['low'].min())
    # df1.columns=[symbol]
    print(df_all.head(5))
    # df = get_fut_info(symbol, df_zero)
    # axes[index].set_title(symbol,fontproperties='SimHei', fontsize=15)
    # df_plot = merge_df(df,df_sz)
    # df.plot(ax=axes[index])
    index=index+1
df_all.plot()
plt.show()
# pic_name="test411.v1.png"
# png_output_dir=".\\analyse_png\\"
# plt.subplots_adjust(hspace=0.5)
# plt.savefig(png_output_dir+pic_name)
