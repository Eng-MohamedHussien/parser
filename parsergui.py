import sys
from PyQt5.QtWidgets import QApplication ,QTextEdit ,QWidget ,QPushButton ,QVBoxLayout ,QHBoxLayout,QMessageBox
from PARSER import *
import os.path

class Notepad(QWidget):
    def __init__(self):
        super(Notepad, self).__init__()
        self.text = QTextEdit(self)
        self.save_button = QPushButton('SAVE')
        self.clear_button = QPushButton('CLEAR')
        self.generate_button = QPushButton('GENERATE')
        self.exit_button = QPushButton('EXIT')
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_text)
        layout.addWidget(self.clear_button)
        self.clear_button.clicked.connect(self.clear_text)
        layout.addWidget(self.generate_button)
        self.generate_button.clicked.connect(self.generate)
        layout.addWidget(self.exit_button)
        self.exit_button.clicked.connect(self.close)
        self.setLayout(layout)
        self.setWindowTitle('Parser Gui')
        self.show()
        

    def clear_text(self):
        self.text.clear()

    def save_text(self):
        with open('input.txt','w') as f:
            my_text = self.text.toPlainText()
            f.write(my_text)

    def generate(self):
        if os.path.isfile('input.txt'):
            try:
                programe()
            except Error as error:
                QMessageBox.about(self, 'Error', error.message)
        else:
            QMessageBox.about(self, 'Error', "No Code entered yet!!")
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    writer = Notepad()
    sys.exit(app.exec_())
