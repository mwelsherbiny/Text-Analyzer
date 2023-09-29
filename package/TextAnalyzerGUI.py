import sys

sys.path.append("package")

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QRadioButton,
    QMessageBox,
    QPlainTextEdit,
    QCheckBox,
)
from PyQt5.QtGui import QFont
from TextAnalyzer import TextAnalyzer


class TextAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # apply style from the css file
        self.setStyleSheet(open("styles.css").read())

        # name the window of the program
        self.setWindowTitle("Text Analyzer")

        # create a grid layout
        self.layout = QGridLayout()

        # create a horizontal layout that can be used to edit the text box
        text_box_options = QHBoxLayout()

        # create a text box
        self.text_box = QPlainTextEdit()
        self.text_box.setPlaceholderText("Type in text")
        self.text_box.setFont(QFont("Monospaced font", 12))

        # create a clear button that removes all text inside the text box
        self.clear_bt = QPushButton("Clear")
        self.clear_bt.setToolTip("Delete all text inside the text box")
        self.clear_bt.clicked.connect(self.on_click_clear)

        # create a correct button that fixes mispelling and grammer errors of text
        self.correct_bt = QPushButton("Correct")
        self.correct_bt.setToolTip("Correct text errors")
        self.correct_bt.clicked.connect(self.on_click_correct)

        # add the buttons to the text_box_options layout
        text_box_options.addWidget(self.clear_bt)
        text_box_options.addWidget(self.correct_bt)

        # create vertical layout for selections
        selection = QVBoxLayout()

        # word count radiobutton
        self.word_count_bt = QRadioButton("Word count", self)
        self.word_count_bt.setFont(QFont("Monospaced font", 12))

        # character count radiobutton
        self.char_count_bt = QRadioButton("Character count", self)
        self.char_count_bt.setFont(QFont("Monospaced font", 12))

        # sentence count radiobutton
        self.sentence_count_bt = QRadioButton("Sentence count", self)
        self.sentence_count_bt.setFont(QFont("Monospaced font", 12))

        # grade level radiobutton
        self.grade_level_bt = QRadioButton("Grade level", self)
        self.grade_level_bt.setFont(QFont("Monospaced font", 12))

        # submit button that starts the processing of text when clicked
        sumbit = QPushButton("Analyze")
        sumbit.setToolTip("Click to extract the data from text")
        sumbit.move(430, 220)
        sumbit.clicked.connect(self.on_click_submit)

        # data displayed when user presses on the submit button
        self.data = QLabel("")

        # add the widgets to the selection layout
        selection.addWidget(self.word_count_bt)
        selection.addWidget(self.char_count_bt)
        selection.addWidget(self.sentence_count_bt)
        selection.addWidget(self.grade_level_bt)
        selection.addWidget(sumbit)

        # add all widgets and layout to the grid layout
        self.layout.addLayout(text_box_options, 0, 0)
        self.layout.addWidget(self.text_box, 1, 0)
        self.layout.addLayout(selection, 1, 1)

        # set the grid layout as the layout for the program
        self.setLayout(self.layout)

    # runs when "clear" button is clicked
    def on_click_clear(self):
        self.text_box.setPlainText("")

    # runs when "correct" button is clicked
    def on_click_correct(self):
        text = self.text_box.toPlainText()
        analyzer = TextAnalyzer(text)
        self.text_box.setPlainText(analyzer.correct_text())

    # runs when "submit" button is clicked
    def on_click_submit(self):
        # clear the data displayed by the previous submit button
        self.data.clear()

        # exctract the text from the text box
        text = self.text_box.toPlainText()
        if not text:
            self.no_text_error()
            return

        # create an analyzer for that text
        analyzer = TextAnalyzer(text)

        # determine the button that was clicked
        if self.word_count_bt.isChecked():
            self.data = QLabel(f"Word count: {analyzer.get_word_count()}", self)
            self.data.setFont(QFont("Monospaced font", 14))
            self.layout.addWidget(self.data, 2, 0)

        elif self.char_count_bt.isChecked():
            self.data = QLabel(f"Character count: {analyzer.get_char_count()}", self)
            self.data.setFont(QFont("Monospaced font", 14))
            self.layout.addWidget(self.data, 2, 0)

        elif self.sentence_count_bt.isChecked():
            self.data = QLabel(
                f"Sentence count: {analyzer.get_sentences_count()}", self
            )
            self.data.setFont(QFont("Monospaced font", 14))
            self.layout.addWidget(self.data, 2, 0)

        elif self.grade_level_bt.isChecked():
            self.data = QLabel(f"Grade Level: {analyzer.get_grade()}", self)
            self.data.setFont(QFont("Monospaced font", 14))
            self.layout.addWidget(self.data, 2, 0)

    # runs when the user submits without typing anything in the text box
    def no_text_error(self):
        error_msg = QMessageBox()
        error_msg.setText(
            "Please enter text",
        )
        error_msg.setWindowTitle("empty text box")
        self.layout.addWidget(error_msg, 1, 0)
