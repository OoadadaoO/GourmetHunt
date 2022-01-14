from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap,QFont, QBrush, QPalette
from GUI.FontSet import FontSet
import sys
from GUI.window.BlogSubWindow import BlogSubWindow
from GUI.window.MenuSubWindow import MenuSubWindow
from GUI.window.RandomSubWindow import RandomSubWindow
from GUI.window.FavoriteSubWindow import FavoriteSubWindow
from GUI.window.LoginDialog import LoginDialog

class TabWindow(QTabWidget):
    def __init__(self):
        super(TabWindow, self).__init__()
        self.setWindowTitle('GourmetHunter')
        self.resize(800, 600)
        tabFont = FontSet(11, True)
        self.setFont(tabFont)
        self.blogSubWindow = BlogSubWindow()
        self.menuSubWindow = MenuSubWindow()
        self.randomSubWindow = RandomSubWindow()
        self.favoriteSubWindow = FavoriteSubWindow()
        self.favoriteSubWindow.onClickedCheckButton()

        self.addTab(self.blogSubWindow, '愛食記獵人')
        self.addTab(self.menuSubWindow, '菜單獵人')
        self.addTab(self.randomSubWindow, '選擇困難救星')
        self.addTab(self.favoriteSubWindow, '我的最愛餐廳')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TabWindow()
    main.show()
    sys.exit(app.exec_())