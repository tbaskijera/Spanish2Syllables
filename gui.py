import sys
from algorithm import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ScrollLabel(QScrollArea):
 
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)
        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)
 
    def setText(self, text):
        self.label.setText(text)

 
def input_text():
    text, pressed = QInputDialog.getText(win, "Input Text", "Text: ", QLineEdit.Normal, "")
    if pressed:
        label.setText(process(text))
        label.adjustSize()
 

def dialog():
    new_list = []
    file, check = QFileDialog.getOpenFileName(None, "Open file", "", "Text Files (*.txt)")
    if check:
        f = open(file, 'r', encoding='utf-8')
        for line in f:       
            for word in line.split(): 
                new_list.append(process(word))
        new_string = ' '.join(new_list)        
        label2.setText(new_string)
 

app = QApplication(sys.argv)
win = QMainWindow()
win.setGeometry(200,200,200,200)

button = QPushButton(win)
button.setText("Add text")
button.setStyleSheet("QPushButton{background-color: lightcoral;}"
                     "QPushButton::hover {background-color: coral;};")
button.clicked.connect(input_text)
button.move(50,110)

button2 = QPushButton(win)
button2.setText("Add file")
button2.setStyleSheet("QPushButton{background-color: lightcoral;}"
                     "QPushButton::hover {background-color: coral;};")
button2.clicked.connect(dialog)
button2.move(50,250)

label = QLabel(win)
label.setText("Empty Text")
label.move(50,150)

label22 = QLabel(win)
label22.setText("Click on <strong>'Add file'</strong> button to upload a file that contains the text that you want to split into syllables.")
label22.move(50, 230)
label22.adjustSize()

label2 = ScrollLabel(win)
label2.setGeometry(50, 300, 900, 400)

label3 = QLabel("Arial", win)
label3.setText("Spanish2Syllables")
label3.setFont(QFont("Arial", 20))
label3.setStyleSheet("font-weight: bold")
label3.adjustSize()
label3.move(360, 40)

win.show()
win.setWindowIcon(QtGui.QIcon('icon.jpg'))
win.setWindowTitle("Spanish2Syllables") 
# win.setStyleSheet("background-color: yellow;")
win.resize(1000, 750)
sys.exit(app.exec_())