from package import TextAnalyzerGUI, TextAnalyzer
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextAnalyzerGUI.TextAnalyzerGUI()
    window.show()
    window.setFixedSize(window.size())
    sys.exit(app.exec_())