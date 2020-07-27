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

def get_symbol_map():
    symbol_map={}
    df=pd.read_excel("all_stock_detail.xlsx")
    for  row in df.iterrows():
        symbol_map[row[1]["stock_num"]]=row[1]["name"]
    return symbol_map

def get_df_from_local(code):
    symbol=code.replace(".","-")
    target_url="http://localhost:8777/api/stockHis/"+symbol
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

today=todayDateStr()
if not os.path.exists(today):
    os.makedirs(today)

industry_list=["白酒","银行","水泥","旅游服务","空运","石油加工","啤酒","保险","证券","食品","化学制药","中成药","半导体"]
symbol_name_map = get_symbol_map()

for industry_str in industry_list:
    symbol_list = get_industry_local(industry_str)
    length= len(symbol_list)
    
    df_all = pd.DataFrame()
    df_excel = pd.DataFrame() # 用于导出当日数据
    row_num = round(length/5+1)
    
    for elem in symbol_list:
        symbol = elem
        name = symbol_name_map[symbol]
        print(symbol)
        df = get_df_from_local(symbol)
        df['symbol']=symbol
        df['name']=name
        min=df['low'].min()
        max=df['high'].max()
        df['guiyi']=(df['close']-min)/(max-min)
        df_excel=df_excel.append(df.tail(1))
        df_all[symbol]=df['guiyi']
    
    df_excel.sort_values("guiyi").to_excel(today+"/"+industry_str+"_"+ today+"_analyse.xlsx")