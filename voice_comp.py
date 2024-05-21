import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from resemblyzer import preprocess_wav, VoiceEncoder
import numpy as np
import os

class WorkerThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, file1_path, file2_path, result_label):
        super().__init__()
        self.file1_path = file1_path
        self.file2_path = file2_path
        self.result_label = result_label

    def run(self):
        similarity_rate = self.compareSounds(self.file1_path, self.file2_path)
        self.progress_signal.emit(similarity_rate)

    def compareSounds(self, sound_1_path, sound_2_path):
        sound_encoder = VoiceEncoder(verbose=False)
        file_1 = preprocess_wav(sound_1_path)
        file_2 = preprocess_wav(sound_2_path)

        encoded_sound1 = sound_encoder.embed_utterance(file_1)
        encoded_sound2 = sound_encoder.embed_utterance(file_2)

        dot_product_size = np.dot(encoded_sound1, encoded_sound2)
        norm_sound1 = np.linalg.norm(encoded_sound1)
        norm_sound2 = np.linalg.norm(encoded_sound2)

        similarity = dot_product_size / (norm_sound1 * norm_sound2) * 100

        color = QColor(Qt.black)
        text = "The likelihood of being the same person is low."

        if similarity < 70:
            color = QColor(Qt.darkYellow)
            text = "The likelihood of being the same person is low."
        elif similarity < 60:
            color = QColor(Qt.red)
            text = "The likelihood of being the same person is very low."
        elif similarity >= 70:
            color = QColor(Qt.darkGreen)
            text = "The likelihood of being the same person is very high."

        self.result_label.setStyleSheet(f"color: {color.name()};")
        self.result_label.setText(text)

        return int(similarity)

class VoiceComparatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.file1_label = QLabel('File 1:')
        self.file2_label = QLabel('File 2:')
        self.result_label = QLabel('Similarity Rate:')
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.file1_button = QPushButton('Select File 1')
        self.file2_button = QPushButton('Select File 2')
        self.compare_button = QPushButton('Compare')

        vbox = QVBoxLayout()
        vbox.addWidget(self.file1_label)
        vbox.addWidget(self.file1_button)
        vbox.addWidget(self.file2_label)
        vbox.addWidget(self.file2_button)
        vbox.addWidget(self.result_label)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.compare_button)

        self.setLayout(vbox)

        self.file1_button.clicked.connect(self.selectFile1)
        self.file2_button.clicked.connect(self.selectFile2)
        self.compare_button.clicked.connect(self.startComparison)

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('VOICE COMPARATOR')
        self.show()

    def selectFile1(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select File 1')
        self.file1_label.setText(f'File 1: {file_path}')

    def selectFile2(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select File 2')
        self.file2_label.setText(f'File 2: {file_path}')

    def startComparison(self):
        file1_path = self.file1_label.text().replace('File 1: ', '')
        file2_path = self.file2_label.text().replace('File 2: ', '')

        if os.path.exists(file1_path) and os.path.exists(file2_path):
            self.worker_thread = WorkerThread(file1_path, file2_path, self.result_label)
            self.worker_thread.progress_signal.connect(self.updateProgressBar)
            self.worker_thread.start()

    def updateProgressBar(self, value):
        self.progress_bar.setValue(value)
        self.result_label.setText(f'Similarity Rate: {value}%')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VoiceComparatorApp()
    sys.exit(app.exec_())
