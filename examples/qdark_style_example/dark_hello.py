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

class TabDemo(QTabWidget):

    def __init__(self,parent=None):
        super(TabDemo,self).__init__(parent)
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.addTab(self.tab1,"Tab1")
        self.addTab(self.tab2,"Tab2")
        self.addTab(self.tab3,"Tab3")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("Tab example")

    def tab1UI(self):
        layout = QFormLayout()
        layout.addRow("姓名",QLineEdit())
        layout.addRow("地址",QLineEdit())
        self.setTabText(0,"联系方式")#?
        self.tab1.setLayout(layout)
    
    def tab2UI(self):
        layout = QFormLayout()
        sex=QHBoxLayout()
        sex.addWidget(QRadioButton("男"))
        sex.addWidget(QRadioButton("女"))
        layout.addRow(QLabel("性别"),sex)
        layout.addRow("生日",QLineEdit())
        self.setTabText(1,"个人详细信息")
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout=QHBoxLayout()
        layout.addWidget(QLabel("科目"))
        layout.addWidget(QCheckBox("物理"))
        layout.addWidget(QCheckBox("高数"))
        self.setTabText(2,"教育程度")
        self.tab3.setLayout(layout)

class WebView(QWebEngineView):
    def __init__(self,parent=None):
        super(WebView,self).__init__()
        url='http://www.ifeng.com'
        self.load(QUrl(url))
        self.show()
        QTimer.singleShot(1000*10,self.close)


# add Dialog Example to check Combox/SpinBox/connect signal
class InterestCalc(QDialog):

    def __init__(self,parent=None):
        super(InterestCalc,self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        print("begin to init_ui")
        principalLabel=QLabel("Pricipal:")
        self.principalSpinBox=QDoubleSpinBox()
        self.principalSpinBox.setRange(1,100000)
        self.principalSpinBox.setValue(100)
        # self.principalSpinBox.setPrefix("元")
        # self.principalSpinBox.setSuffix(" a")

        rateLabel=QLabel("Rate:")
        self.rateSpinBox=QDoubleSpinBox()
        self.rateSpinBox.setRange(1,100)
        self.rateSpinBox.setValue(5)
        self.rateSpinBox.setPrefix("")
        self.rateSpinBox.setSuffix(" %")

        yearLabel=QLabel("Year:")
        self.yearCombBox=QComboBox()
        self.yearCombBox.addItem("1 year")
        self.yearCombBox.addItems([
            "{0} years".format(x)  for x in range(2,30)
        ])

        amountLabel=QLabel("Amount")
        self.amountLabel=QLabel()

        
        grid=QtWidgets.QGridLayout()
        grid.addWidget(principalLabel,0,0)
        grid.addWidget(self.principalSpinBox,0,1)
        grid.addWidget(rateLabel,1,0)
        grid.addWidget(self.rateSpinBox,1,1)
        grid.addWidget(yearLabel,2,0)
        grid.addWidget(self.yearCombBox,2,1)
        grid.addWidget(amountLabel,3,0)
        grid.addWidget(self.amountLabel,3,1)

        self.setLayout(grid)
        self.setWindowTitle("利率计算样例")
        self.principalSpinBox.valueChanged.connect(self.updateUI)
        self.rateSpinBox.valueChanged.connect(self.updateUI)
        self.yearCombBox.currentIndexChanged.connect(self.updateUI)

    def updateUI(self):
        principal=self.principalSpinBox.value()
        rate=self.rateSpinBox.value()
        year=self.yearCombBox.currentIndex()+1
        value=principal*((1+rate/100)**year)
        self.amountLabel.setText("RMB {0:.2f}".format(value))

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
    # window = MainWindow()
    # window = InterestCalc()
    #window=WebView()
    window=TabDemo()

    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window.show()
    app.exec_()