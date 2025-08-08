from PySide6.QtWidgets import (
    QDockWidget, QTabWidget, QWidget,
    QVBoxLayout, QLabel
)

class RightDock(QDockWidget):
    def __init__(self, parent=None):
        super().__init__("Right Dock", parent)
        self.setFixedWidth(200)
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #555;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background: #1a1a1a;
                color: #ddd;
                padding: 6px;
                border: 1px solid #444;
            }
            QTabBar::tab:selected {
                background: #2a2a2a;
            }
        """)

        self.create_train_tools_tab()
        self.create_visual_tools_tab()
        self.setWidget(self.tabs)
        self.setTitleBarWidget(QWidget(self))

    def create_train_tools_tab(self):
        train_tools = QWidget()
        layout = QVBoxLayout(train_tools)

        label = QLabel("Train Tools Area")
        label.setStyleSheet("color: #ccc; font-size: 13px;")
        layout.addWidget(label)

        layout.addStretch()
        self.tabs.addTab(train_tools, "Train Tools")

    def create_visual_tools_tab(self):
        visual_tools = QWidget()
        layout = QVBoxLayout(visual_tools)

        label = QLabel("Visualizer Tools Area")
        label.setStyleSheet("color: #ccc; font-size: 13px;")
        layout.addWidget(label)

        layout.addStretch()
        self.tabs.addTab(visual_tools, "Visualizer Tools")
