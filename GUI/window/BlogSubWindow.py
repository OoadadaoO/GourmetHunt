from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont, QBrush, QPalette, QKeyEvent
from PyQt5.QtCore import QEvent, Qt
from GUI.FontSet import FontSet
from crawl.find_artical import find_artical
import sys

class BlogSubWindow(QWidget):
    def __init__(self):
        super(BlogSubWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('愛食記獵人')
        self.resize(800,600)
        self.mainLayout = QVBoxLayout()
        self.typeLayout = QGridLayout()
        self.showLayout = QFormLayout()

        self.mainLayout.addLayout(self.typeLayout)
        self.mainLayout.addLayout(self.showLayout)
        self.setLayout(self.mainLayout)

        self.text = QLabel()
        self.keywordType = QLineEdit()
        self.checkButton = QPushButton()

        # textFont = FontSet(12, True)
        self.text.setText('Keyword:')
        # self.text.setFont(textFont)
        self.text.setBuddy(self.keywordType)
        keywordFont = FontSet(11)
        self.keywordType.setPlaceholderText('place, food, type...')
        self.keywordType.setFont(keywordFont)
        self.keywordType.returnPressed.connect(self.onClickedCheckButton)
        # checkButtonFont = FontSet(12, True)
        self.checkButton.setText('Search')
        # self.checkButton.setFont(checkButtonFont)
        self.checkButton.setEnabled(False)

        self.typeLayout.addWidget(self.text, 0, 0)
        self.typeLayout.addWidget(self.keywordType, 0, 1)
        self.typeLayout.addWidget(self.checkButton, 0, 3)

        self.checkButton.clicked.connect(self.onClickedCheckButton)
        self.keywordType.textChanged.connect(self.inChangedKeywordType)

    def crawlData(self,keyword):
        demoList = find_artical(keyword)
        # demoList = [['title','https://www.google.com/'],['title','link'],['title','link'],['title','link']]
        return demoList

    def inChangedKeywordType(self):
        if self.keywordType.text() != '':
            self.checkButton.setEnabled(True)
        else:
            self.checkButton.setEnabled(False)

    def onClickedCheckButton(self):
        # 清空上次搜尋結果
        if not self.showLayout.isEmpty():
            for i in reversed(range(self.showLayout.count())):
                self.showLayout.itemAt(i).widget().deleteLater()
        # 取得輸入文字
        keyword = self.keywordType.text()
        # 清空輸入欄的文字
        # self.keywordType.clear()
        # 顯示文字
        instruction = f"'{keyword}' 的搜尋結果："
        self.instruction = QLabel()
        self.instruction.setText(instruction)
        self.showLayout.addRow(self.instruction)
        # 呼叫爬蟲方法進行爬蟲
        dataList = self.crawlData(keyword)
        # 將爬蟲資料顯示
        for i in dataList:
            tiitleFont = FontSet(10, False)
            urlFont = FontSet(9, False)
            self.title = QLabel()
            self.url = QLabel()
            self.title.setText(i[0])
            self.title.setFont(tiitleFont)
            self.url.setText(f'<a href = "{i[1]}">{i[1]}</a>')
            self.url.setFont(urlFont)
            self.url.setOpenExternalLinks(True)
            self.showLayout.addRow(self.title,self.url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BlogSubWindow()
    main.show()
    sys.exit(app.exec_())