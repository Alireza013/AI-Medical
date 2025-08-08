from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

def create_viewer_split_page():
    page = QWidget()
    page.setStyleSheet("background-color: #1e1e1e;")
    layout = QHBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(1)

    left_sidebar = QLabel("📂 Image Sidebar")
    left_sidebar.setStyleSheet("color: orange; background-color: #222; padding: 20px;")
    left_sidebar.setFixedWidth(250)

    right_view = QLabel("🖼️ Main Image Display")
    right_view.setStyleSheet("color: white; background-color: #111; padding: 20px;")

    left_sidebar.setStyleSheet("color: orange; background-color: #111; padding: 10px;")
    right_view.setStyleSheet("color: white; background-color: #111; padding: 10px;")

    layout.addWidget(left_sidebar)
    layout.addWidget(right_view)
    return page
