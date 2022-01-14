from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from GUI.FontSet import FontSet
from crawl.find_menu import find_menu
import sys

class MenuSubWindow(QWidget):
    def __init__(self):
        super(MenuSubWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('菜單獵人')
        self.resize(800,600)
        self.mainLayout = QVBoxLayout()
        self.typeLayout = QGridLayout()
        self.showLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.typeLayout)
        self.mainLayout.addLayout(self.showLayout)
        self.setLayout(self.mainLayout)

        self.text = QLabel()
        self.keywordType = QLineEdit()
        self.checkButton = QPushButton()

        # textFont = FontSet(12, True)
        self.text.setText('Restaurant:')
        # self.text.setFont(textFont)
        keywordFont = FontSet(11)
        self.keywordType.setPlaceholderText('restaurant name')
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
        demoPath = find_menu(keyword)
        # demoPath = "./image/demo.png"
        return demoPath

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
        instruction = f'{keyword} 的菜單'
        instructionFont = FontSet(20, True)
        self.instruction = QLabel()
        self.instruction.setText(instruction)
        self.instruction.setFont(instructionFont)
        self.instruction.setAlignment(Qt.AlignCenter)
        self.showLayout.addWidget(self.instruction,1)
        # 呼叫爬蟲方法進行爬蟲
        imagePath = self.crawlData(keyword)
        # 將爬蟲圖片顯示
        imagePixmap = QPixmap(imagePath)
        imagePixmap = imagePixmap.scaled(799,600)
        self.image = QLabel(self)
        self.image.setPixmap(imagePixmap)
        self.image.setAlignment(Qt.AlignCenter)
        self.showLayout.addWidget(self.image,4)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MenuSubWindow()
    main.show()
    sys.exit(app.exec_())
