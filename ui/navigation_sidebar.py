from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class NavigationBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nav_callback = None
        self.setStyleSheet("background-color: #111;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(8)

        self.buttons = {}
        self.current_active = None

        self.home_button = self.create_button("Home")
        self.layout.addWidget(self.home_button)
        self.buttons["Home"] = self.home_button

        self.dynamic_buttons_container = QWidget()
        self.dynamic_layout = QVBoxLayout(self.dynamic_buttons_container)
        self.dynamic_layout.setContentsMargins(0, 0, 0, 0)
        self.dynamic_layout.setSpacing(5)
        self.layout.addWidget(self.dynamic_buttons_container)

        self.set_active_button("Home")

    def set_nav_callback(self, callback):
        self.nav_callback = callback

    def create_button(self, name):
        button = QPushButton(name)
        button.setFixedHeight(36)
        button.setStyleSheet(self.button_style(inactive=True))
        button.clicked.connect(lambda: self.set_active_button(name))
        button.clicked.connect(lambda: self.nav_callback(name) if self.nav_callback else None)
        return button

    def set_active_button(self, name):
        for btn_name, btn in self.buttons.items():
            btn.setStyleSheet(self.button_style(inactive=(btn_name != name)))
        self.current_active = name
        if self.nav_callback:
            self.nav_callback(name)

    def button_style(self, inactive=True):
        if inactive:
            return """
                QPushButton {
                    background-color: #1e1e1e;
                    color: #ccc;
                    border: 1px solid #333;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #333;
                    color: #FF8C00;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: #333;
                    color: #FF8C00;
                    border: 1px solid #FF8C00;
                    border-radius: 5px;
                }
            """

    def set_dynamic_buttons(self, button_definitions):
        for i in reversed(range(self.dynamic_layout.count())):
            widget = self.dynamic_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for name, callback in button_definitions:
            button = self.create_button(name)
            button.clicked.connect(callback)
            self.dynamic_layout.addWidget(button)
            self.buttons[name] = button

        if self.current_active == "Home":
            self.set_active_button("Home")
