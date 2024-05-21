import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import subprocess

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HIT - Human Identification Tool. Compare faces & voices.")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.addButton("VOICE COMPARATOR", "python3 voice_comp.py")
        self.addButton("FACE COMPARATOR", "python3 face_comp.py")

        self.setLayout(self.layout)

    def addButton(self, text, command):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.startProcess(command))
        self.layout.addWidget(button)

    def startProcess(self, command):
        subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()
    dashboard.show()
    sys.exit(app.exec_())
