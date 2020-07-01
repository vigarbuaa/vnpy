import numpy as np
import talib
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt

# 模拟数据,0629改为实际数据
# df = pd.DataFrame(np.random.rand(18,4))
# df.columns=['open','high','low','close']
# print(df)
# result_aroonosc = talib.AROONOSC(df.high, df.low, 4)
# df['aroonosc']=result_aroonosc
# print(df)
# integer = talib.CDLHAMMER(df.open, df.high, df.low, df.close)
# print(integer)


def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())


def download_data(code,date):
    # 获取指定日期的指数、股票数据
    # stock_rs = bs.query_all_stock(date)
    # stock_df = stock_rs.get_data()
    data_df = pd.DataFrame()
    # for code in stock_df["code"]:
    print("Downloading :" + code)
    k_rs = bs.query_history_k_data_plus(code, "date,code,open,high,low,close,volume,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST", "2020-01-01", date)
    data_df = data_df.append(k_rs.get_data())
    return data_df

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
    print(code_list)
    return code_list

# download data and calc AD/ADOSC 

# filter AD >10000 save it to file

bs.login()
get_all_code()
bs.logout()
#symbol="sh.600859"
#date_str = todayDateStr()
## df2=download_data("sz.002142",date_str)
#df2=download_data(symbol,date_str)
#integer = talib.AD(df2.high, df2.low, df2.close,df2.volume)
#df2['AD']=integer
#real = talib.ADOSC(df2.high, df2.low, df2.close, df2.volume, fastperiod=3, slowperiod=10)
#df2['ADOSC']=real
#print(type(df2))
#print(df2.dtypes)
# df2.to_csv(symbol+".csv")

#fig, axes = plt.subplots(3, 1,figsize=(15,10))
#plt.title(summary, fontproperties='SimHei', fontsize=15)
#ax0=axes[0]
#ax0.set_title(symbol,fontproperties='SimHei', fontsize=15)
#df2['close'].astype('float64').plot(ax=axes[0])
#df2['AD'].astype('float64').plot(ax=axes[1])
#df2['ADOSC'].astype('float64').plot(ax=axes[2])
#pic_name=symbol+".png"
#plt.subplots_adjust(hspace=0.5)
#plt.savefig(pic_name)