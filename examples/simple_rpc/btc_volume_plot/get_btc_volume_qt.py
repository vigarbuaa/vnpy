from __future__ import print_function
from __future__ import absolute_import
from time import sleep
import os
import random
import pyqtgraph as pg
from rpc_server import RpcClient
import pandas as pd
from datetime import datetime
import warnings
import sys
import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore  import *
import requests
from datetime import datetime, timedelta

class InterestCalc(QDialog):

    def __init__(self,parent=None):
        super(InterestCalc,self).__init__(parent)
        self.init_ui()
        self.init_engine()

    def init_engine(self):
        req_address = "tcp://119.27.160.141:2019"
        sub_address = "tcp://119.27.160.141:9102"
        self.engine = DataEngine()
        self.engine.subscribe_topic("")
        self.engine.start(req_address, sub_address)

    def init_ui(self):
        print("begin to init_ui")
        self.init_graph()
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=3 * 30)

        self.start_date_edit = QtWidgets.QDateEdit(
            QtCore.QDate(
                start_dt.year,
                start_dt.month,
                start_dt.day
            )
        )
        self.end_date_edit = QtWidgets.QDateEdit(
            QtCore.QDate.currentDate()
        )

        self.query_btn = QtWidgets.QPushButton(self)
        self.query_btn.setText("查询")
        form = QtWidgets.QFormLayout()
        form.addRow("开始时间",self.start_date_edit);
        form.addRow("结构时间",self.end_date_edit);
        form.addRow("",self.query_btn);
        self.query_btn.clicked.connect(self.get_data)
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.chart)
        self.setLayout(vbox)

    def init_graph(self):
        self.chart=HisChart()
        self.chart.setMinimumWidth(300)

    def get_data(self):
        print("=========begin==========")
        start = self.start_date_edit.date().toPyDate()
        end = self.end_date_edit.date().toPyDate()
        date_range = pd.date_range(start,end)
        range_length= len(date_range)
        for elem in date_range:
            date_str = str(elem).split(" ")[0].replace("-","")
            print(date_str)
            ret = self.engine.getBtcData(date_str)
            print(ret)
        print("=========end==========")

        

#    def updateUI(self):
#        principal=self.principalSpinBox.value()
#        rate=self.rateSpinBox.value()
#        year=self.yearCombBox.currentIndex()+1
#        value=principal*((1+rate/100)**year)
#        self.amountLabel.setText("RMB {0:.2f}".format(value))

class HisChart(pg.GraphicsWindow):
    def __init__(self):
        """"""
        super().__init__(title="History Chart")
        self.dates = {}
        self.init_ui()
    
    def init_ui(self):
        """"""
        pg.setConfigOptions(antialias=True)
        self.balance_plot = self.addPlot(
            title="---",
            axisItems={"bottom": DateAxis(self.dates, orientation="bottom")})
        # Add curves and bars on plot widgets

        self.balance_curve = self.balance_plot.plot(
            pen=pg.mkPen("#ffc107", width=3)
        )

    def set_data(self, df):
        if df is None:
            return

        count = len(df)
        self.dates.clear()
        for n, date in enumerate(df.index):
            self.dates[n] = date
        self.balance_curve.set_data(df['close'])

class DateAxis(pg.AxisItem):
    """Axis for showing date data"""

    def __init__(self, dates: dict, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.dates = dates

    def tickStrings(self, values, scale, spacing):
        """"""
        strings = []
        for v in values:
            dt = self.dates.get(v, "")
            strings.append(str(dt))
        return strings

# 业务class，远程取数据
class DataEngine(RpcClient):
    """
    Test RpcClient
    """
    client_name = ""
    def __init__(self):
        super(DataEngine, self).__init__()
        self.client_name=os.getpid()

    # 接到消息后的回调
    def callback(self, topic, data):
        print(f"client {self.client_name} received topic:{topic}, data:{data}")


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow()
    window = InterestCalc()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window.show()
    app.exec_()

#    while 1:
#        print(tc.add(random.randint(1,100), random.randint(1,200)))
#        sleep(2)
#        print(tc.sub(random.randint(1,100), random.randint(1,200)))
#        sleep(2)
#        print("-----------call ---tushare test ---------")
#        df=tc.getBtcData('20180806')
#        print(df)
#        print("result: "+ str(df))
#        sleep(2)
