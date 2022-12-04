import re
import sys

VOWELS = ["a", "á", "e", "é", "i", "í", "o", "ó", "u", "ú", "ü"]
STRONG_VOWELS = ["a", "á", "e", "é", "o", "ó", "í", "ú", "ü"]
WEAK_VOWELS = ["i", "u"]
CONSONANTS = ["x", "j", "t", "s", "c", "g", "l",
              "f", "ll", "m", "r", "rr", "p", "h", "y", "ñ", "b", "d", "k", "n", "q", "v", "z", "ch", "w"]
UNALLOWED = ["pr", "pl", "br", "bl", "fr",
             "fl", "gr", "gl", "cr", "cl", "dr", "tr", "tl"]
STRONG_STRONG_VOWEL_PAIRS = ["ae", "ao", "ea", "eo", "oa", "oe"] # dali treba dodati parove sa naglascima
WEAK_WEAK_VOWEL_PAIRS = ["iu", "ui"]
STRONG_WEAK_VOWEL_PAIRS = ["ai", "ei", "oi", "au",
                           "eu", "ou", "ia", "ie" "io", "ua", "ue", "uo"] # dali treba dodati parove sa naglascima
WEAK_STRONG_WEAK_VOWEL_TRIFTONG = ["iai", "iái","iau", "iáu", "iei", "iéi", "ieu", "iéu", "ioi", "iói", "iou", "ióu",
                                   "uai", "uái", "uau", "uáu", "uei", "uéi", "ueu", "uéu", "uoi", "uói", "uou", "uóu"]                   
INSEPARABLE = ["ns", "bs", "rs", "ps", "gs", "cs", "ks", "ds", "ts", "ms", "ls", "vs", "fs"]
STRONG_WEAK_TO_STRONG_VOWEL_PAIRS = ["aí", "aú", "aü", "eí", "eú", "eü", "oí", "oú", "oü",
                                    "ía", "úa", "üa", "íe", "úe", "üe", "ío", "úo", "üo"]

test_list = ["casa", "oprimo", "obrero",  "aflojar", "cafre", "hablando", "agrandar", "aglutinar", 
            "acróbata", "aclamar", "cuadro", "cuatro", "atlas", "atlalilco", "inseparable", "artista",
            "comedlo", "ponedla", "empleados", "englobar", "constitución", "instaurar", "obstinado",
            "instalar", "perspectiva", "aéreo", "pelear", "leo", "aire", "europa", "ásia", "cuidado",
            "ruidoso", "triunfante", "bioinformática", "radioisótopo", "asociáis", "buey", "había", "país", "reúno"]


def is_vowel(char):
    return char == 'V'


def is_consonant(char):
    return char == 'C'


def check_offset(string, point):
    count = 0
    for i in range(point):
        if string[i] == "-":
            count += 1
    return count


def formalize(string):
    formalized_string = ""
    for letter in string:
        if letter in VOWELS:
            formalized_string += "V"
        elif letter in CONSONANTS:
            formalized_string += "C"
        else:
            formalized_string += letter
    return formalized_string


"""
def rule_1(formalism):
    formatted = ""
    for count, letter in enumerate(formalism):
        if is_consonant(letter) and count not in [0, 1]:
            if (is_vowel(formalism[count-1]) and is_vowel(formalism[count+1])):
                formatted += '-' + letter
        else:
            formatted += letter
    return formatted
"""


def rule_1(formalism):
    return re.sub('VCV', 'V-CV', formalism)


def rule_2(formalism, string):
    pattern = re.finditer("VCCV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        consonant1 = pattern_start+1
        consonant2 = pattern_start+2
        offset = check_offset(formalism, pattern_start)
        c_pair = string[consonant1 - offset] + string[consonant2 - offset]
        if c_pair in UNALLOWED:
            formalism = re.sub('VCCV', 'V-CCV', formalism, 1)
        else:
            formalism = re.sub('VCCV', "VC-CV", formalism, 1)
    return formalism


def rule_3(formalism, string):
    pattern = re.finditer("VCCCV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        consonant1 = pattern_start+1
        consonant2 = pattern_start+2
        consonant3 = pattern_start+3
        offset = check_offset(formalism, pattern_start)
        end_two = string[consonant2 - offset] + string[consonant3 - offset]
        first_two = string[consonant1 - offset] + string[consonant2 - offset]
        if end_two in UNALLOWED:
            formalism = re.sub('VCCCV', 'VC-CCV', formalism, 1)
        elif first_two in INSEPARABLE:
            formalism = re.sub('VCCCV', "VCC-CV", formalism, 1)
    return formalism


def rule_4(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in STRONG_STRONG_VOWEL_PAIRS:
            formalism = re.sub("VV", "V-V", formalism, 1)
    return formalism


def rule_5(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in STRONG_WEAK_VOWEL_PAIRS:
            formalism = re.sub("VV", "VV", formalism, 1)
    return formalism


def rule_6(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in WEAK_WEAK_VOWEL_PAIRS:
            formalism = re.sub("VV", "VV", formalism, 1)
    return formalism


def rule_7(formalism, string):
    pattern = re.finditer("VVV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in WEAK_STRONG_WEAK_VOWEL_TRIFTONG:
            formalism = re.sub("VVV", "VVV", formalism, 1)
    return formalism


def rule_8(formalism, string):
    pattern = re.finditer("VV", formalism)
    if pattern is None:
        return formalism
    for object in pattern:
        pattern_start = object.start()
        vowel1 = pattern_start
        vowel2 = pattern_start+1
        offset = check_offset(formalism, pattern_start)
        v_pair = string[vowel1-offset] + string[vowel2-offset]
        if v_pair in STRONG_WEAK_TO_STRONG_VOWEL_PAIRS:
            formalism = re.sub("VV", "V-V", formalism, 1)
    return formalism


def process(string):
    formalism = formalize(string)
    formalism = rule_1(formalism)
    #formalism = rule_2(formalism, string)
    formalism1 = rule_2(formalism, string)
    formalism1 = rule_2(formalism1, string)
    formalism = rule_1(formalism1) 
    formalism = rule_3(formalism, string)
    formalism = rule_4(formalism, string)
    formalism = rule_4(formalism, string)
    formalism = rule_5(formalism, string)
    formalism = rule_6(formalism, string)
    formalism = rule_7(formalism, string)
    formalism = rule_8(formalism, string)
    #print(formalism)
    return formalism


# def test(list):
#     for item in list:
#         print("procesira se ", item, ": ")
#         process(item)

# test(test_list)

# process("inseparable")
# process("inssparable") # ovaj radi dobro jer ima suglasnik umjesto e


# def input_text():
#     text = input("Unesi tekst koji želiš rastaviti na slogove: ")
#     return text

# process(input_text())



import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

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
    file, check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "Text Files (*.txt)")
    if check:
        f = open(file)
        proc = f.read()
        label2.setText(process(proc))
 
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






