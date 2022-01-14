from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from GUI.FontSet import FontSet
import sys

class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()
        self.initUI()
        self.username = ''

    def initUI(self):
        self.setWindowTitle('使用者登入')
        self.resize(200,100)
        self.mainLayout = QVBoxLayout()
        self.typeLayout = QGridLayout()
        self.btnLayout = QHBoxLayout()

        self.mainLayout.addLayout(self.typeLayout)
        self.mainLayout.addLayout(self.btnLayout)
        self.setLayout(self.mainLayout)

        self.usernameText = QLabel()
        self.usernameType = QLineEdit()
        self.visitorButton = QPushButton()
        self.userLoginButton = QPushButton()

        usernameTextFont = FontSet(10, True)
        self.usernameText.setText('Username:')
        self.usernameText.setFont(usernameTextFont)
        usernameTypeFont = FontSet(9)
        self.usernameType.setPlaceholderText('your name')
        self.usernameType.setFont(usernameTypeFont)
        visitorButtonFont = FontSet(10, True)
        self.visitorButton.setText('Visitor Mode')
        self.visitorButton.setFont(visitorButtonFont)
        userLoginButtonFont = FontSet(10, True)
        self.userLoginButton.setText('User Login')
        self.userLoginButton.setFont(userLoginButtonFont)
        self.userLoginButton.setEnabled(False)
        self.typeLayout.addWidget(self.usernameText, 0, 0)
        self.typeLayout.addWidget(self.usernameType, 0, 1)
        self.btnLayout.addWidget(self.visitorButton)
        self.btnLayout.addWidget(self.userLoginButton)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = LoginDialog()
    main.show()
    sys.exit(app.exec_())
