from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap,QFont, QBrush, QPalette
from PyQt5.QtCore import Qt
import sys
from GUI.TabWindow import TabWindow
from GUI.window.FavoriteSubWindow import FavoriteSubWindow
from GUI.window.LoginDialog import LoginDialog
from GUI.FontSet import FontSet

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GourmetHunter')
        self.setWindowIcon(QIcon('./GUI/image/windowIconWhite.png'))
        self.resize(800,800)
        self.setFixedSize(800, 800)
        self.mainLayout = QVBoxLayout()
        self.userLayout = QGridLayout()
        self.tabLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.userLayout, 0)
        self.mainLayout.addLayout(self.tabLayout, 1)
        self.setLayout(self.mainLayout)

        # 使用者設定區塊
        self.welcomeText = QLabel()
        self.statusLabel = QLabel()
        self.modeButton = QPushButton()

        welcomeTextFont = FontSet(28, True, 'Jokerman')
        self.welcomeText.setText(' GOURMET HUNTER')
        self.welcomeText.setFont(welcomeTextFont)
        self.welcomeText.setAlignment(Qt.AlignLeft)
        self.welcomeText.setAlignment(Qt.AlignVCenter)
        statusLabelFont = FontSet(16, True)
        self.statusLabel.setText('Visitor Mode')
        self.statusLabel.setFont(statusLabelFont)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        modeButtonFont = FontSet(9, True)
        self.modeButton.setText('LOG IN')
        self.modeButton.setFont(modeButtonFont)

        self.userLayout.addWidget(self.welcomeText, 0, 0, 2, 3)
        self.userLayout.addWidget(self.statusLabel, 0, 3, 1, 1)
        self.userLayout.addWidget(self.modeButton, 1, 3, 1, 1)

        # 分隔線
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.mainLayout.addWidget(self.line, 0)

        # 選項卡區塊
        self.tabWindow = TabWindow()

        self.tabLayout.addWidget(self.tabWindow)

        background = QPalette()
        backgroundImage = QPixmap('./GUI/image/background.png')
        backgroundImage = backgroundImage.scaled(self.width(), self.height())
        background.setBrush(self.backgroundRole(), QBrush(backgroundImage))
        self.setPalette(background)

        self.modeButton.clicked.connect(self.openLoginDialog)

    def openLoginDialog(self):
        self.loginDialog = LoginDialog()
        self.loginDialog.show()
        self.loginDialog.usernameType.textChanged.connect(self.inChangedUsernameType)
        self.loginDialog.visitorButton.clicked.connect(self.onClickedVisitorButton)
        self.loginDialog.userLoginButton.clicked.connect(self.onClickedUserLoginButton)

    def inChangedUsernameType(self):
        # 當無輸入文字時，visitorButton方可使用
        if self.loginDialog.usernameType.text() == '':
            self.loginDialog.userLoginButton.setEnabled(False)
            self.loginDialog.visitorButton.setEnabled(True)
        # 當輸入文字不為空且沒有空白時，userLoginButton方可使用
        elif not self.loginDialog.usernameType.text().isspace() and self.loginDialog.usernameType.text() != '':
            self.loginDialog.userLoginButton.setEnabled(True)
            self.loginDialog.visitorButton.setEnabled(False)

    def onClickedVisitorButton(self):
        username = 'visitor'
        self.loginDialog.close()

        statusLabelFont = QFont()
        statusLabelFont.setPointSize(12)
        statusLabelFont.setBold(True)
        self.statusLabel.setText('Visitor Mode')
        self.statusLabel.setFont(statusLabelFont)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.modeButton.setText('LOG IN')

        self.favoriteSubWindow = FavoriteSubWindow(username)
        self.tabWindow.insertTab(3, self.favoriteSubWindow, '我的最愛餐廳')
        self.tabWindow.removeTab(4)
        self.favoriteSubWindow.onClickedCheckButton()

    def onClickedUserLoginButton(self):
        username = self.loginDialog.usernameType.text()
        self.loginDialog.close()

        statusLabelFont = QFont()
        statusLabelFont.setPointSize(12)
        statusLabelFont.setBold(True)
        self.statusLabel.setText(username)
        self.statusLabel.setFont(statusLabelFont)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.modeButton.setText('LOG IN AS ANOTHER')

        self.favoriteSubWindow = FavoriteSubWindow(username)
        self.tabWindow.insertTab(3, self.favoriteSubWindow, username + '的最愛餐廳')
        self.tabWindow.removeTab(4)
        self.favoriteSubWindow.onClickedCheckButton()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())