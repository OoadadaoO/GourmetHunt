from PyQt5.QtGui import QFont

def FontSet(size, bold = False, font = '微軟正黑體'):
    Font = QFont()
    Font.setFamily(font)
    Font.setPointSize(size)
    Font.setBold(bold)
    return Font