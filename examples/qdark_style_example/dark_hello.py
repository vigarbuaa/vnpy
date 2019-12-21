from datetime import datetime
import warnings
import sys
import qdarkstyle
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore  import *
import requests

class MainWindow(QMainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.init_ui()
        self.setTitle()
    
    def init_ui(self):
        self.setWindowTitle("Q dark style hello")
        self.resize(450,347)
        self.groupBox = QtWidgets.QGroupBox(self)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 431, 251))
        #self.groupBox.setObjectName("groupBox")

        self.weatherComboBox=QtWidgets.QComboBox(self.groupBox)
        self.weatherComboBox.setGeometry(QtCore.QRect(100,30,221,21))
        self.weatherComboBox.setObjectName("WeatherComboBox")
        self.weatherComboBox.addItem("")
        self.weatherComboBox.addItem("")
        self.weatherComboBox.addItem("")
        self.resultText = QtWidgets.QTextEdit(self.groupBox)
        self.resultText.setGeometry(QtCore.QRect(10,60,411,181))
        self.resultText.setObjectName("resultText")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 30, 72, 21))

        self.label.setObjectName("label")

        self.queryBtn = QtWidgets.QPushButton(self)
        self.queryBtn.setGeometry(QtCore.QRect(90, 300, 93, 28))
        self.clearBtn = QtWidgets.QPushButton(self)
        self.clearBtn.setGeometry(QtCore.QRect(230, 300, 93, 28))
        self.clearBtn.setObjectName("clearBtn")

        self.clearBtn.clicked.connect(self.clearResult)
        self.queryBtn.clicked.connect(self.queryWeather)

    def setTitle(self):
        self.groupBox.setTitle("查询天气")
        self.label.setText("城市")
        self.weatherComboBox.setItemText(0,  "北京")
        self.weatherComboBox.setItemText(1,  "天津")
        self.weatherComboBox.setItemText(2,  "上海")
        self.queryBtn.setText( "查询")
        self.clearBtn.setText( "清空")

    def transCityName(self,cityName):
        cityCode=""
        if cityName=="北京":
            cityCode = '101010100'
        elif cityName=="天津":
            cityCode = '101030100'
        elif cityName=="上海":
            cityCode = '101020100'
        return cityCode

    def queryWeather(self):
        print("begin to query weather")
        cityName = self.weatherComboBox.currentText()
        cityCode=self.transCityName(cityName)

        rep= requests.get('http://www.weather.com.cn/data/sk/'+cityCode+".html")
        rep.encoding="utf-8"
        print(rep.json())
        result=rep.json()
        self.resultText.setText(str(result))

    def clearResult(self):
        print("clear result")
        self.resultText.clear()


if __name__=="__main__":
# create the application and the main window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window.show()
    app.exec_()