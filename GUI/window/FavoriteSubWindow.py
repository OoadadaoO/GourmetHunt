from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import Qt
from GUI.FontSet import FontSet
from favorite.favorite import storage, tidy, resShow
import csv
import sys


class FavoriteSubWindow(QWidget):
    def __init__(self, username = 'visitor'):
        super(FavoriteSubWindow, self).__init__()
        uniUsername = str(username.encode('unicode_escape'))
        uniUsername = uniUsername.replace("'", '')
        uniUsername = uniUsername.replace('\\', '')
        with open(f'./favorite/csv/{uniUsername}.csv', 'a') as csvfile:
            pass
        self.initUI(username)
        self.username = username

    def initUI(self, username):
        self.setWindowTitle('我的最愛')
        self.resize(800,600)
        self.mainLayout = QVBoxLayout()
        self.newLayout = QHBoxLayout()
        self.sortLayout = QVBoxLayout()
        self.nameTypeLayout = QFormLayout()
        self.categoryTypeLayout = QFormLayout()
        self.selectLayout = QHBoxLayout()
        self.showLayout = QGridLayout()

        self.newLayout.addLayout(self.nameTypeLayout)
        self.newLayout.addLayout(self.categoryTypeLayout)
        self.sortLayout.addLayout(self.selectLayout)
        self.sortLayout.addLayout(self.showLayout)
        self.setLayout(self.mainLayout)

        # 新增我的最愛的區塊
        self.nameText = QLabel()
        self.nameType = QLineEdit()
        self.categoryText = QLabel()
        self.categoryType = QLineEdit()
        self.storeButton = QPushButton()

        self.nameText.setText('Name:')
        nameTypeFont = FontSet(11)
        self.nameType.setPlaceholderText('restaurant name')
        self.nameType.setFont(nameTypeFont)
        self.categoryText.setText('Category:')
        categoryFont = FontSet(11)
        self.categoryType.setPlaceholderText('category')
        self.categoryType.setFont(categoryFont)
        self.storeButton.setText('Store')
        self.storeButton.setEnabled(False)

        self.nameTypeLayout.addRow(self.nameText, self.nameType)
        self.categoryTypeLayout.addRow(self.categoryText, self.categoryType)
        self.newLayout.addWidget(self.storeButton)

        self.mainLayout.addLayout(self.newLayout, 0)

        # 分隔線
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.mainLayout.addWidget(self.line, 0)

        # 查詢我的最愛的區塊
        # self.categoryAll = ['全部', '燒烤', '火鍋', '其他']
        self.categoryAll = tidy(username)

        self.categoryList = QComboBox()
        self.checkButtom = QPushButton()
        self.showTable = QTableWidget()
        self.scrollBar = QScrollBar()

        self.categoryList.addItems(self.categoryAll)
        self.checkButtom.setText('Sort')
        self.showTable.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.showTable.setShowGrid(False)
        self.showTable.setColumnCount(3)
        self.showTable.setRowCount(100)
        self.showTable.setHorizontalHeaderLabels(['Name', 'Category', 'Other'])
        width = int(self.showTable.width()/3)
        self.showTable.setColumnWidth(0, width)
        self.showTable.setColumnWidth(1, width)
        self.showTable.setColumnWidth(2, width)
        self.showTable.setVerticalScrollBar(self.scrollBar)

        self.selectLayout.addWidget(self.categoryList, 1)
        # self.selectLayout.addWidget(self.checkButtom, 0)
        self.showLayout.addWidget(self.showTable)

        self.mainLayout.addLayout(self.sortLayout, 1)

        self.nameType.textChanged.connect(self.inChangedType)
        self.categoryType.textChanged.connect(self.inChangedType)
        self.storeButton.clicked.connect(self.onClickedStoreButton)
        self.categoryList.currentTextChanged.connect(self.onClickedCheckButton)
        self.checkButtom.clicked.connect(self.onClickedCheckButton)


    def sortData(self, username = 'visitor', category = '全部'):
        # demoList = [['demo name0', ['demo category0']], ['demo name1', ['demo category1']], ['demo name2', ['demo category2']]]
        demoList = resShow(username, category)
        return demoList

    def inChangedType(self):
        if self.nameType.text() != '' and self.categoryType.text() != '':
            self.storeButton.setEnabled(True)
        else:
            self.storeButton.setEnabled(False)

    def onClickedStoreButton(self):
        username = self.username
        restaurant = self.nameType.text()
        category = self.categoryType.text()
        storage(username, restaurant, category)
        self.nameType.clear()
        self.categoryType.clear()
        self.categoryAll = tidy(username)
        self.categoryList.clear()
        self.categoryList.addItems(self.categoryAll)
        self.onClickedCheckButton()
        return None

    def onClickedCheckButton(self):
        # 清空上次搜尋結果
        self.showTable.clear()
        self.showTable.setHorizontalHeaderLabels(['Name', 'Category', 'Other'])
        # 取得篩選條件
        username, category = self.username, self.categoryList.currentText()
        # 取得資料值
        dataList = self.sortData(username, category)
        for subList in dataList:
            for element in subList:
                if type(element) == str:
                    elementItem = QTableWidgetItem(element)
                    self.showTable.setItem(dataList.index(subList), subList.index(element), elementItem)
                elif type(element) == list:
                    newElement = element[0]
                    for i in element[1:]:
                        newElement += '、' + i
                    elementItem = QTableWidgetItem(newElement)
                    self.showTable.setItem(dataList.index(subList), subList.index(element), elementItem)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = FavoriteSubWindow()
    main.show()
    sys.exit(app.exec_())
