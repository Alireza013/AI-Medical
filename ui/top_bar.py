from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QToolButton, QHBoxLayout

class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_buttons = {}
        self.menu_callback = None
        self.init_ui()

    def set_menu_callback(self, callback):
        self.menu_callback = callback

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                border-bottom: 1px solid #333;
            }
        """)
        self.create_top_bar()
        self.setFixedHeight(50)

    def create_top_bar(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(30)

        self.menu_buttons = {
            "Imaging Tools": self.create_menu_button("Imaging Tools"),
            "Model Training": self.create_menu_button("Model Training"),
            "Plugin Extensions": self.create_menu_button("Plugin Extensions")
        }

        for name, button in self.menu_buttons.items():
            layout.addWidget(button)
            button.clicked.connect(lambda _, n=name: self.set_active_menu(n))

        layout.addStretch()
        self.setLayout(layout)

    def create_menu_button(self, text):
        btn = QToolButton(self)
        btn.setText(text)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(self.default_style())
        return btn

    def default_style(self):
        return """
            QToolButton {
                background-color: transparent;
                color: #FF8C00;
                font-size: 12px;
                font-weight: bold;
                border: none;
                padding: 4px 8px;
            }
            QToolButton:hover {
                background-color: #444;
            }
        """

    def active_style(self):
        return """
            QToolButton {
                background-color: #444;
                color: #FF8C00;
                font-size: 13px;
                font-weight: bold;
                border: none;
                padding: 4px 8px;
            }
        """

    def set_active_menu(self, selected_name):
        for name, btn in self.menu_buttons.items():
            btn.setStyleSheet(self.active_style() if name == selected_name else self.default_style())

        if self.menu_callback:
            self.menu_callback(selected_name)
