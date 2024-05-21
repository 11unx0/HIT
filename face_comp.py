import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import face_recognition

class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FACE COMPARATOR")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.image_1_label = QLabel("Image 1")
        self.layout.addWidget(self.image_1_label)

        self.addButton("Select Image 1", self.selectImage1)
        self.image_2_label = QLabel("Image 2")
        self.layout.addWidget(self.image_2_label)

        self.addButton("Select Image 2", self.selectImage2)
        self.compare_button = QPushButton("Compare Faces")
        self.compare_button.clicked.connect(self.compareFaces)
        self.layout.addWidget(self.compare_button)

        self.result_label = QLabel()
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def addButton(self, text, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.layout.addWidget(button)

    def selectImage1(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Image 1', '', 'Image Files (*.png *.jpg *.jpeg)')
        if file_path:
            self.image_1_path = file_path
            self.displayImage(self.image_1_label, file_path)

    def selectImage2(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select Image 2', '', 'Image Files (*.png *.jpg *.jpeg)')
        if file_path:
            self.image_2_path = file_path
            self.displayImage(self.image_2_label, file_path)

    def displayImage(self, label, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaledToWidth(300)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setScaledContents(True)

    def compareFaces(self):
        if hasattr(self, 'image_1_path') and hasattr(self, 'image_2_path'):
            face_1_image = face_recognition.load_image_file(self.image_1_path)
            face_2_image = face_recognition.load_image_file(self.image_2_path)

            face_1_encodings = face_recognition.face_encodings(face_1_image)
            face_2_encodings = face_recognition.face_encodings(face_2_image)

            if face_1_encodings and face_2_encodings:
                distance = face_recognition.face_distance([face_1_encodings[0]], face_2_encodings[0])
                similarity_percentage = (1 - distance[0]) * 100
                result_text = f"Similarity Rate: {similarity_percentage:.2f}%\n"

                face_1_locations = face_recognition.face_locations(face_1_image)
                face_2_locations = face_recognition.face_locations(face_2_image)

                result_text += f"Face 1 Locations: {face_1_locations}\n"
                result_text += f"Face 2 Locations: {face_2_locations}"

                if similarity_percentage > 45:
                    result_text += "\n# Similarity > 45% # There is a possibility that these are the same person."

                self.result_label.setText(result_text)
            else:
                self.result_label.setText("No face found in one or both images.")
        else:
            self.result_label.setText("Please select both images.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FaceRecognitionApp()
    ex.show()
    sys.exit(app.exec_())
