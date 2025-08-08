from PySide6.QtWidgets import (
    QDockWidget, QTabWidget, QWidget,
    QVBoxLayout, QLabel, QScrollArea
)

class LeftDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Left Dock", parent)
        self.setFixedWidth(200)
        self.init_ui()
        self.setStyleSheet("""
            QDockWidget {
                background-color: #111;
                border: 1px solid #444;  /* lighter gray */
            }
        """)

    def init_ui(self):
        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #555;  /* subtle visible gray */
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background: #1a1a1a;
                color: #ddd;  /* near white for visibility */
                padding: 6px;
                border: 1px solid #444;
            }
            QTabBar::tab:selected {
                background: #2a2a2a;
            }
        """)

        self.create_main_tools_tab()
        self.create_image_tools_tab()
        self.setWidget(self.tabs)
        self.setTitleBarWidget(QWidget(self))

    def create_main_tools_tab(self):
        scroll = QScrollArea()
        main_tools = QWidget()
        layout = QVBoxLayout(main_tools)

        label = QLabel("Main Tools Area")
        label.setStyleSheet("color: #ccc; font-size: 13px;")
        layout.addWidget(label)
        layout.addStretch()

        scroll.setWidget(main_tools)
        scroll.setWidgetResizable(True)
        self.tabs.addTab(scroll, "Main Tools")

    def create_image_tools_tab(self):
        image_tools = QWidget()
        layout = QVBoxLayout(image_tools)

        label = QLabel("Image Details Tools Area")
        label.setStyleSheet("color: #ccc; font-size: 13px;")
        layout.addWidget(label)
        layout.addStretch()

        self.tabs.addTab(image_tools, "Image Details Tools")
