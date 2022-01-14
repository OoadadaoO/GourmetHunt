from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import Qt
from GUI.FontSet import FontSet
from crawl.random_rest import randomrestaurant
import sys

class RandomSubWindow(QWidget):
    def __init__(self):
        super(RandomSubWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('選擇困難救星')
        self.resize(800,600)
        self.mainLayout = QVBoxLayout()
        self.typeLayout = QGridLayout()
        self.showLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.typeLayout)
        self.mainLayout.addLayout(self.showLayout)
        self.setLayout(self.mainLayout)

        self.placeText = QLabel()
        self.placeType = QLineEdit()
        self.keywordText = QLabel()
        self.keywordType = QLineEdit()
        self.distanceText = QLabel()
        self.distanceType = QLineEdit()
        self.priceText = QLabel()
        self.priceSelec = QComboBox()
        self.rateText = QLabel()
        self.rateSelec = QComboBox()
        self.checkButton = QPushButton()

        self.placeText.setText('Place:')
        placeTypeFont = FontSet(11)
        self.placeType.setPlaceholderText('place')
        self.placeType.setFont(placeTypeFont)
        self.keywordText.setText('Keyword:')
        placeKeywordType = FontSet(11)
        self.keywordType.setPlaceholderText('food, type...')
        self.keywordType.setFont(placeKeywordType)
        self.distanceText.setText('Distance:')
        distanceTypeFont = FontSet(11)
        self.distanceType.setPlaceholderText('meter')
        self.distanceType.setFont(distanceTypeFont)
        self.priceText.setText('Price:')
        priceSelecFont = FontSet(11)
        self.priceSelec.addItems(['\tAny', '$\tLow', '$$\tMedium', '$$$\tHigh'])
        self.priceSelec.setFont(priceSelecFont)
        self.priceSelec.setCurrentIndex(0)
        self.rateText.setText('Rate:')
        rateSelecFont = FontSet(11)
        self.rateSelec.addItems(['\tAny', '★\t(1)', '★★\t(2)', '★★★\t(3)', '★★★★\t(4)', '★★★★★\t(5)'])
        self.rateSelec.setFont(rateSelecFont)
        self.rateSelec.setCurrentIndex(0)
        self.checkButton.setText('Search')
        self.checkButton.setEnabled(False)

        self.typeLayout.addWidget(self.placeText, 0, 0)
        self.typeLayout.addWidget(self.placeType, 0, 1)
        self.typeLayout.addWidget(self.keywordText, 1, 0)
        self.typeLayout.addWidget(self.keywordType, 1, 1)
        self.typeLayout.addWidget(self.distanceText, 2, 0)
        self.typeLayout.addWidget(self.distanceType, 2, 1)
        self.typeLayout.addWidget(self.priceText, 3, 0)
        self.typeLayout.addWidget(self.priceSelec, 3, 1)
        self.typeLayout.addWidget(self.rateText, 4, 0)
        self.typeLayout.addWidget(self.rateSelec, 4, 1)
        self.typeLayout.addWidget(self.checkButton, 4, 3)

        self.checkButton.clicked.connect(self.onClickedCheckButton)
        self.placeType.textChanged.connect(self.inChangedKeywordType)

    def crawlData(self, place, keyword, distance, money, rate):
        demoDict = randomrestaurant(place, keyword, distance, money, rate)

        # demoDict = {'name': 'Restaurant Name', 'url': 'https://www.google.com/', 'path': './image/demo.png'}
        return demoDict

    def price(self, origin):
        if origin == '\tAny': return 0
        elif origin == '$\tLow': return 1
        elif origin == '$$\tMedium': return 2
        elif origin == '$$$\tHigh': return 3

    def rate(self, origin):
        if origin == '\tAny': return 0
        elif origin == '★\t(1)': return 1
        elif origin == '★★\t(2)': return 2
        elif origin == '★★★\t(3)': return 3
        elif origin == '★★★★\t(4)': return 4
        elif origin == '★★★★★\t(5)': return 5

    def inChangedKeywordType(self):
        if self.placeType.text() != '':
            self.checkButton.setEnabled(True)
        else:
            self.checkButton.setEnabled(False)

    def onClickedCheckButton(self):
        # 清空上次搜尋結果
        if not self.showLayout.isEmpty():
            for i in reversed(range(self.showLayout.count())):
                self.showLayout.itemAt(i).widget().deleteLater()
        # 取得輸入文字
        place = self.placeType.text()
        keyword = self.keywordType.text()
        distance = self.distanceType.text()
        price = self.price(self.priceSelec.currentText())
        rate = self.rate(self.rateSelec.currentText())
        # 清空輸入欄的文字
        # self.placeType.clear()
        # self.keywordType.clear()
        # self.distanceType.clear()
        # self.priceType.clear()
        # 顯示文字
        instruction = f"為您推薦以下餐廳："
        self.instruction = QLabel()
        self.instruction.setText(instruction)
        self.showLayout.addWidget(self.instruction, 0)
        # 呼叫爬蟲方法進行爬蟲
        dataDict = self.crawlData(place, keyword, distance, price, rate)
        if type(dataDict) == str:
            self.error = QLabel()
            self.instruction.setText(dataDict)
            self.showLayout.addWidget(self.error, 1)
        else:
            # 顯示餐廳名稱
            nameFont = QFont()
            nameFont.setFamily('微軟正黑體')
            nameFont.setPointSize(20)
            nameFont.setBold(True)
            self.name = QLabel()
            self.name.setText(dataDict['name'])
            self.name.setFont(nameFont)
            self.name.setAlignment(Qt.AlignCenter)
            self.showLayout.addWidget(self.name,0)
            # 顯示餐廳連結
            self.link = QLabel()
            self.link.setText('<a href = "' + dataDict['url'] + '">' + dataDict['url'] + '</a>')
            self.link.setOpenExternalLinks(True)
            self.link.setAlignment(Qt.AlignCenter)
            self.showLayout.addWidget(self.link,0)
            # # 將爬蟲圖片顯示
            self.imagePath = QPixmap(dataDict['path'])
            self.image = QLabel(self)
            self.image.setPixmap(self.imagePath)
            self.image.setAlignment(Qt.AlignCenter)
            self.showLayout.addWidget(self.image,1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = RandomSubWindow()
    main.show()
    sys.exit(app.exec_())
