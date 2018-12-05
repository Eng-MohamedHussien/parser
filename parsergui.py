import sys
from PyQt5 import QtWidgets

def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    w.setWindowTitle('Parser Gui')
    w.show()
    sys.exit(app.exec_())

window()
