# encoding: UTF-8
import numpy as np
import talib,json
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt
from urllib import request
import plotly.graph_objects as go
import plotly.offline as py
from plotly.subplots import make_subplots
import copy

#----------------------------------------------------------------------
def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

def get_all_code_local():
    df=pd.read_excel("all_stock_detail.xlsx")
    return df['stock_num'].tolist()

def get_industry_local(industry):
    df=pd.read_excel("all_stock_detail.xlsx")
    return df[df["industry"]==industry]["stock_num"].tolist()

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
    # ret = df.sort_values('date')
    ret = df
    ret['date_str']=pd.to_datetime(ret['date'])
    # ret=ret.sort_values('date_str')
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

industry_str = "银行"
symbol_list = get_industry_local(industry_str)
length= len(symbol_list)

today=todayDateStr()
if not os.path.exists(today):
    os.makedirs(today)

# 改为分拔画图,5个一组画
index=0
#data=[]
df_all = pd.DataFrame()
df_excel = pd.DataFrame() # 用于导出当日数据
row_num = round(length/5+1)
fig = make_subplots(rows=row_num, cols=1)

for elem in symbol_list:
    symbol = elem
    print(symbol)
    df = get_df_from_local(symbol)
    df['symbol']=symbol
    df['guiyi']=(df['close']-df['low'].min())/(df['high'].max()-df['low'].min())
    df_excel=df_excel.append(df.tail(1))
    print(df.head(5))
    df_all[symbol]=df['guiyi']
    print(df_all.head(5))
    # trace = go.Scatter(x=df_all.index,y=df_all[symbol],mode="lines+markers",name=symbol)
    index=index+1
    print(round(index/5 +1))
    fig.add_trace(go.Line(x=df_all.index, y=df_all[symbol],mode="lines+markers", name=symbol), row=round(index/5+1), col=1)
    # data.append(trace)

print(df_excel)
df_excel.to_excel(today+"/"+industry_str+"_"+ today+"_analyse.xlsx")
fig.update_layout(height=3000, width=1200)
fig.show()
# py.iplot(data)



# https://www.pianshen.com/article/5500341648/