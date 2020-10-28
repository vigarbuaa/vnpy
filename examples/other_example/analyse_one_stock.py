import numpy as np
import talib
import pandas as pd
import baostock as bs
import os, time, json, sys, traceback, logging, getopt
import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif']=['KaiTi']
mpl.rcParams['axes.unicode_minus']=False

df = pd.read_excel("C:/Users/vigar/Documents/GitHub/vnpy_vigar/examples/other_example/600859_stock_k_data.xlsx",sheet_name="600859_stock_k_data",header=0,index_col=0)
df2=df['turn']
df2.plot(kind="line",figsize=(15,9),title="浦发换手率",grid=True,fontsize=13)

df3=df['amount']/100000000
df3.plot(kind="hist",figsize=(15,9),title="浦发交易额",grid=True,fontsize=13)

df3.plot(kind="box",figsize=(15,9),title="浦发交易额",grid=True,fontsize=13)

df4=df[['open','high','low','close']]

df4.plot(kind="line",subplots=True,sharex=True,sharey=True,layout=(2,2),figsize=(10,8),title="走势图",grid=True,fontsize=13)
