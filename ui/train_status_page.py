import threading
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit


class TrainStatusPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout(self)

        self.status_label = QLabel("Train Status View")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.status_label.setStyleSheet("""
            color: #FF8C00;
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addWidget(self.status_label)
