import numpy as np
import talib,json
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt
from urllib import request
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

def download_data(code,begin_date,end_date):
    # 获取指定日期的指数、股票数据
    # stock_rs = bs.query_all_stock(date)
    # stock_df = stock_rs.get_data()
    data_df = pd.DataFrame()
    print("Downloading :" + code)
    k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST", begin_date, end_date)
    data_df = data_df.append(k_rs.get_data())
    return data_df

def get_all_code_local():
    df=pd.read_excel("all_stock_detail.xlsx")
    return df['stock_num'].tolist()

# def get all stock list
def get_all_code():
    rs = bs.query_all_stock(day="2018-06-28")
    print('query_all_stock respond error_code:' + rs.error_code)
    print('query_all_stock respond error_msg:' + rs.error_msg)
# 打印结果集
    code_list = []
    while (rs.error_code == '0') & rs.next():
     # 获取一条记录，将记录合并在一起
        code_list.append(rs.get_row_data()[0])
    # print(code_list)
    return code_list

# plot
def save_plt(df,date,symbol):
    summary=date+"_"+symbol
    fig, axes = plt.subplots(7, 1,figsize=(15,10))
    plt.title(summary, fontproperties='SimHei', fontsize=15)
    ax0=axes[0]
    ax0.set_title(symbol,fontproperties='SimHei', fontsize=15)
    df['close'].astype('float64').plot(ax=axes[0])
    df['ad'].astype('float64').plot(ax=axes[1])
    df['adosc'].astype('float64').plot(ax=axes[2])
    df['adxr'].astype('float64').plot(ax=axes[3])
    df['cci'].astype('float64').plot(ax=axes[4])
    df['mfi'].astype('float64').plot(ax=axes[5])
    df['rsi'].astype('float64').plot(ax=axes[6])
    pic_name=symbol+".png"
    plt.subplots_adjust(hspace=1.5)
    plt.savefig(date+"/"+pic_name)

def get_df_from_local(code):
    symbol=code.replace(".","-")
    target_url="http://localhost:8088/api/stockHis/"+symbol
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
    print(ret.head(4))
    return ret 

def draw(df):
    # 创建一个4行、1列的带子图绘图区域，并分别给子图加上标题
    # fig = make_subplots(rows=3, cols=2, subplot_titles=["Close", "volume"])
    fig = make_subplots(rows=5, cols=2)
    fig.add_trace(go.Line(x=df.index, y=df["close"], name="Close"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["volume"], fillcolor="red", fill='tozeroy', line={"width": 0.5, "color": "red"}, name="Volume"), row=1, col=2)
    fig.add_trace(go.Bar(x=df.index, y=df["amount"],  name="Amount"), row=2, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["cci"],  name="CCI"), row=2, col=2)
    fig.add_trace(go.Bar(x=df.index, y=df["rsi"],  name="RSI"), row=3, col=1)
    fig.add_trace(go.Bar(x=df.index, y=df["adx"],  name="ADX"), row=3, col=2)
    fig.add_trace(go.Bar(x=df.index, y=df["mfi"],  name="MFI"), row=4, col=1)
    fig.add_trace(go.Line(x=df.index, y=df["dif"],  name="MACD_diff"), row=4, col=2)
    fig.add_trace(go.Line(x=df.index, y=df["dem"],  name="MACD_dem"), row=4, col=2)
    fig.add_trace(go.Bar(x=df.index, y=df["histogram"],  name="MACD_histogram"), row=4, col=2)
    fig.add_trace(go.Line(x=df.index, y=df["cdl3doutside"],  name="CDL3OUTSIDE"), row=5, col=1)
    fig.add_trace(go.Line(x=df.index, y=df["cdl3whitesoldiers"],  name="cdl3whitesoldiers"), row=5, col=2)
    # fig.add_trace(go.Bar(x=df.index, y=df["amount"],  name="Amount"), row=2, col=1)
    # 把图表放大些，默认小了点
    fig.update_layout(height=1000, width=1000)

    # 将绘制完的图表，正式显示出来
    fig.show()

# 类似这种玩法
# http://www.iwencai.com/stockpick/search?ts=1&f=1&qs=stockhome_topbar_click&w=mfi
def add_talib_zhibiao(df):
    # add cci and +-100 line
    cci= talib.CCI(df.high, df.low, df.close, 14)
    df['cci']=cci
    #名称：Three Outside Up/Down 三外部上涨和下跌   
    cdl3doutside = talib.CDL3OUTSIDE(df.open, df.high, df.low, df.close)
    df['cdl3doutside']=cdl3doutside
    # 三个白兵，指上涨
    cdl3whitesoldiers = talib.CDL3WHITESOLDIERS(df.open, df.high, df.low, df.close)
    df['cdl3whitesoldiers']=cdl3whitesoldiers
    
    rsi = talib.RSI(df.close, timeperiod=14)
    df['rsi']=rsi
    adx = talib.ADX(df.high, df.low, df.close, timeperiod=14)
    df['adx']=adx
    mfi = talib.MFI(df.high, df.low, df.close, df.volume, timeperiod=14)
    df['mfi']=mfi
    dif, dem, histogram = talib.MACD(df.close, fastperiod=12, slowperiod=26, signalperiod=9)
    df['dif']=dif
    df['dem']=dem
    df['histogram']=histogram
    return df

# bs.login()
# code_list= get_all_code_local()
# print(code_list)
# today=todayDateStr()
# if not os.path.exists(today):
    # os.makedirs(today)
df = get_df_from_local("sh.600859")
df = add_talib_zhibiao(df)
print(df.index)
print(df.columns)
draw(df)
print(df.head(5))
print(df.tail(5))


#index=0
#for elem in code_list:
#    try:
#        df=download_data(elem,"2020-01-01",today)
#        adosc= talib.ADOSC(df.high, df.low, df.close, df.volume, fastperiod=3, slowperiod=10)
#        df['adosc']=adosc
#        adxr = talib.ADXR(df.high, df.low, df.close, timeperiod=14)
#        df['adxr']=adxr
#        mfi = talib.MFI(df.high, df.low, df.close, df.volume, timeperiod=14)
#        df['mfi']=mfi
#        cci= talib.CCI(df.high, df.low, df.close, 14)
#        df['cci']=cci
#        rsi = talib.RSI(df.close, 10)
#        df['rsi']=rsi
#        ad= talib.AD(df.high, df.low, df.close,df.volume)
#        df['ad']=ad
#        if(rsi.values[-1]>80):
#            df.to_csv(today+"/"+elem+".csv")
#            save_plt(df,today,elem)
#    except:
#        traceback.print_exc
#bs.logout()
