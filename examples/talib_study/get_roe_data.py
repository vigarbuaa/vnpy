"""
    vigarbuaa 
    取得ROE
"""
import baostock as bs
import pandas as pd
import os, time, json, sys, traceback, logging, getopt

bs.login()
def todayDateStr():
    return  time.strftime("%Y-%m-%d",time.localtime())

# 取出stock自2018年以来的各季度roe，并重新命名 example: 2018-1-roe
def get_roe(stock,year_num,quarter_num):
    dupont_list = []
    rs_dupont = bs.query_dupont_data(code=stock, year=year_num, quarter=quarter_num)
    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
    df = result_profit[['code','statDate','dupontROE']]
    if(len(df)>0):
        return  df['dupontROE'][0]
    else:
        return 0

def get_all_roe(stock):
    dict={}
    year_array=[2018,2019,2020]
    quarter_array = [1,2,3,4]
    for e_year in year_array:
        for e_qua in quarter_array:
            key=str(e_year)+"_"+str(e_qua)+"_ROE"
            # print("----"+key)
            # print(str(e_year)+"-"+str(e_qua))
            roe = get_roe(stock,e_year,e_qua)
            # ret = pd.concat([ret,df_elem])
            dict[key]=roe
    df=pd.DataFrame.from_dict(dict,orient='index')
    df=df.T
    df.index=[stock]
    return df

# 循环取出所有stock的roe
def get_roe_df(stock_array):
    df_ret= pd.DataFrame() 
    for elem in stock_array:
        print("-get roe--" + elem)
        df_temp = get_all_roe(elem)
        df_ret=pd.concat([df_ret,df_temp])
    return df_ret

df_roe=get_roe_df(stock_list)
print(df_roe.index)
df.set_index("stock_num",inplace=True)
date_str = todayDateStr()
#date_str = "2020-06-05"
#df2=download_data(date_str)
df2=download_stock_data(date_str,stock_list)
df2.rename(columns={"code":"stock_num"},inplace=True)
df2.set_index("stock_num",inplace=True)
df_all=df.join(df2).join(df_roe)
file_name = "trace_stock_v2"+date_str+".xlsx"
df_all.to_excel(file_name)
bs.logout()

df_today = pd.read_excel(file_name)
df_2=df_today[["2018_1_ROE","2018_2_ROE","2018_3_ROE","2018_4_ROE","2019_1_ROE","2019_2_ROE","2019_3_ROE","2019_4_ROE","2020_1_ROE"]]
df_today["roe_agv"]=df_2.mean(axis=1)
df_today["roe"]=df_today["roe_agv"].map(lambda x:format(x,".2%"))
df_today.sort_values("roe_agv", ascending=False).to_excel(date_str+"sort_roe_.v3.xlsx")
