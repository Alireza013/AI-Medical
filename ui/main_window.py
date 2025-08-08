import sys
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (
    QMainWindow, QStackedWidget, QWidget, QFileDialog, QApplication,
    QHBoxLayout, QVBoxLayout, QPushButton, QLabel
)

from interactors.abstract_interactor_style import AbstractInteractorStyle
from ui.top_bar import TopBar

from ui.left_dock import LeftDock
from ui.right_dock import RightDock
from ui.visualizer_page import VisualizerPage
from ui.navigation_sidebar import NavigationBar
from ui.train_status_page import TrainStatusPage
from ui.image_details_page import ImageDetailsPage
from ui.split_viewer_page import create_viewer_split_page
from interactors.segmentation.polygon_segmentation_tool import PolygonSegmentationTool

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drag_pos = QPoint()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(1100, 700)
        self.setStyleSheet("background-color: #1e1e1e;")
        self.current_nav_selection = "Home"
        self.current_menu_selection = ""
        self.active_tool = None  # 'polygon' or None
        
        self.setup_strategies()
        self.setup_ui()

    def setup_ui(self):
        self.top_bar = TopBar(self)
        self.setMenuWidget(self.top_bar)

        self.top_bar.set_menu_callback(self.handle_topbar_selection)

        self.train_page = TrainStatusPage(self)
        self.image_page = ImageDetailsPage(self)
        self.visualizer_page = VisualizerPage(self)
        self.viewer_split_page = create_viewer_split_page()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.train_page)
        self.stacked_widget.addWidget(self.image_page)
        self.stacked_widget.addWidget(self.visualizer_page)
        self.stacked_widget.addWidget(self.viewer_split_page)

        self.blank_page = QWidget()
        self.stacked_widget.addWidget(self.blank_page)

        self.left_dock = LeftDock(self)
        self.right_dock = RightDock(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.left_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.right_dock)

        # Sidebar
        self.navigation_sidebar = NavigationBar(self)

        self.toggle_button = QPushButton("☰")
        self.toggle_button.setFixedSize(36, 36)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #FF8C00;
                font-size: 18px;
                font-weight: bold;
                border: 1px solid #FF8C00;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

        self.toggle_button.clicked.connect(self.toggle_sidebar)

        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(5, 5, 5, 5)
        self.sidebar_layout.setSpacing(10)
        self.sidebar_layout.addWidget(self.toggle_button,
                                    alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.sidebar_layout.addWidget(self.navigation_sidebar)
        self.sidebar_layout.addStretch()

        self.sidebar_widget = QWidget()
        self.sidebar_widget.setLayout(self.sidebar_layout)
        self.sidebar_widget.setFixedWidth(140)

        self.sidebar_animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        self.sidebar_animation.setDuration(300)
        self.sidebar_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.sidebar_expanded = True

        # Top box
        self.top_buttons_layout = QHBoxLayout()
        self.top_buttons_layout.setContentsMargins(20, 20, 20, 10)
        self.top_buttons_layout.setSpacing(12)

        self.empty_top_box = QWidget()
        self.empty_top_box.setFixedHeight(180)
        self.empty_top_box.setStyleSheet("background-color: #252525; border-bottom: 1px solid #333333;")
        self.empty_top_box.setLayout(self.top_buttons_layout)

        self.bottom_container = QWidget()
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(20, 5, 20, 20)
        self.bottom_layout.setSpacing(12)
        self.bottom_container.setLayout(self.bottom_layout)
        self.bottom_container.setFixedHeight(350)
        self.bottom_container.setStyleSheet("background-color: #202020; border-top: 1px solid #333;")
        self.bottom_container.setVisible(False)

        self.empty_top_container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(10, 30, 10, 0)
        container_layout.setSpacing(0)
        container_layout.addWidget(self.empty_top_box)
        self.empty_top_container.setLayout(container_layout)

        self.central_stack_container = QVBoxLayout()
        self.central_stack_container.setContentsMargins(3, 1, 3, 1)
        self.central_stack_container.setSpacing(0)
        self.central_stack_container.addWidget(self.empty_top_container)
        self.central_stack_container.addWidget(self.stacked_widget)
        self.central_stack_container.addWidget(self.bottom_container)

        self.central_stack_widget = QWidget()
        self.central_stack_widget.setLayout(self.central_stack_container)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(self.left_dock)
        main_layout.addWidget(self.central_stack_widget)
        main_layout.addWidget(self.right_dock)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.connect_signals()
        self.show_home_page()
        
    def setup_strategies(self):
        self.top_bar_strategies = {
            "Imaging Tools": self.populate_imaging_tools_menu,
            "Model Training": self.populate_model_training_menu,
            "Plugin Extensions": self.populate_plugin_extensions_menu,
        }

    def activate_default_interactor(self):
        default_style = AbstractInteractorStyle(self.visualizer_page.viewer)
        self.visualizer_page.viewer.image_interactor.SetInteractorStyle(default_style)
        self.visualizer_page.viewer.Render()
        self.active_tool = None

    def handle_polygon_toggle(self):
        if self.active_tool == 'polygon':
            self.activate_default_interactor()
            return

        if self.active_tool:
            self.activate_default_interactor()

        polygon_tool = PolygonSegmentationTool(self.visualizer_page.viewer)
        self.visualizer_page.viewer.image_interactor.SetInteractorStyle(polygon_tool)
        # current_style = self.visualizer_page.viewer.interactor.GetInteractorStyle()
        # print("Current Interactor Style:", type(current_style).__name__)
        polygon_tool.On()
        self.visualizer_page.viewer.Render()
        self.active_tool = 'polygon'

    def handle_topbar_selection(self, name):
        self.current_menu_selection = name
        self.current_nav_selection = "Home"

        strategy = self.top_bar_strategies.get(name)
        if strategy:
            strategy()

        self.navigation_sidebar.set_active_button("Home")
        self.show_home_page()

    def populate_model_training_menu(self):
        self.navigation_sidebar.set_dynamic_buttons([
            ("Visualizer", self.show_visualizer_page),
            ("Train Status", self.show_train_page)
        ])
        self.show_home_page()

    def populate_imaging_tools_menu(self):
        self.navigation_sidebar.set_dynamic_buttons([
            ("Open Viewer Mode", lambda: self.switch_page(self.viewer_split_page, "Viewer", False)),
            ("Filter", lambda: None),
            ("Segment", lambda: None),
            ("Image Details", self.show_image_page)
        ])
        self.show_home_page()

    def populate_plugin_extensions_menu(self):
        self.navigation_sidebar.set_dynamic_buttons([])
        self.show_home_page()

    def on_navigation_item_selected(self, name):
        self.current_nav_selection = name
        self.show_home_page()

    def show_home_page(self):
        self.clear_top_buttons()

        nav = getattr(self, "current_nav_selection", "Home")
        # menu = getattr(self, "current_menu_selection", "")

        if nav == "Home":
            self.render_home_buttons([
                ("Import File", self.handle_file_open),
                ("Export File", lambda: print("Export Clicked")),
                ("Save Workstation", lambda: print("Save Clicked"))
            ])
        elif nav == "Segment":
            self.render_home_buttons([
                ("Import File", self.handle_file_open),
                ("Polygon", lambda: self.handle_polygon_toggle()),
                ("Save Workstation", lambda: print("Save Clicked"))
            ])
        else:
            self.bottom_container.setVisible(False)

    def render_ai_diagnosis_top(self):
        label = QLabel("Drop Image Here")
        label.setFixedSize(320, 120)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #888;
                font-weight: bold;
                border: 2px dashed #FF8C00;
                border-radius: 10px;
            }
        """)
        run_btn = QPushButton("Run")
        run_btn.setFixedSize(120, 36)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF8C00;
                color: black;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ffa733;
            }
        """)
        self.top_buttons_layout.addWidget(label)
        self.top_buttons_layout.addStretch()
        self.top_buttons_layout.addWidget(run_btn)

    def render_home_buttons(self, buttons):
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2b2b2b;
                    border: 1px solid #FF8C00;
                    color: #FF8C00;
                    font-weight: bold;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
            """)
            btn.clicked.connect(slot)
            self.top_buttons_layout.addWidget(btn)

    def clear_top_buttons(self):
        while self.top_buttons_layout.count():
            item = self.top_buttons_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def toggle_sidebar(self):
        self.sidebar_animation.setStartValue(140 if self.sidebar_expanded else 50)
        self.sidebar_animation.setEndValue(50 if self.sidebar_expanded else 140)
        self.sidebar_animation.start()
        self.sidebar_expanded = not self.sidebar_expanded
        self.navigation_sidebar.setVisible(self.sidebar_expanded)

    def connect_signals(self):
        self.navigation_sidebar.set_nav_callback(self.on_navigation_item_selected)
        self.visualizer_page.image_loaded.connect(self.image_page.update_details)

    def switch_page(self, page, title, show_docks_tools):
        if page:
            self.stacked_widget.setCurrentWidget(page)
        if hasattr(self.top_bar, 'title_label'):
            self.top_bar.title_label.setText(f"{title} View")
        self.left_dock.setVisible(show_docks_tools)
        self.right_dock.setVisible(show_docks_tools)
        self.clear_top_buttons()

    def handle_file_open(self):
        folder = QFileDialog.getExistingDirectory(self, "Select DICOM Folder", "")

        if folder:
            self.visualizer_page.load_image(folder)
            self.switch_page(self.visualizer_page, "Visualizer", True)

    def render_ai_diagnosis_bottom(self):
        while self.bottom_layout.count():
            item = self.bottom_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        viewer = QLabel("Viewer")
        viewer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        viewer.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                color: #FF8C00;
                font-weight: bold;
                border: 1px solid #444;
                border-radius: 8px;
            }
        """)
        viewer.setMinimumWidth(400)

        text_box = QLabel("Diagnosis Text Box.")
        text_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        text_box.setStyleSheet("""
            QLabel {
                background-color: #1e1e1e;
                color: #ccc;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
            }
        """)

        self.bottom_layout.addWidget(viewer, 1)
        self.bottom_layout.addWidget(text_box, 2)
        self.bottom_container.setVisible(True)

    def show_train_page(self):
        self.switch_page(self.train_page, "Train Status", True)

    def show_image_page(self):
        self.switch_page(self.image_page, "Image Details", True)

    def show_visualizer_page(self):
        self.switch_page(self.visualizer_page, "Visualizer", True)

    # def handle_polygon_toggle(self, checked):
    #
    #     renderer = self.visualizer_page.viewer.renderer if self.visualizer_page.viewer else None
    #     interactor = self.visualizer_page.interactor
    #     print(checked)
    #
    #     if renderer and interactor:
    #         print(f'in renderer and interactor.')
    #         if checked:
    #             print('in checked on mainwindow')
    #             self.polygon_interactor_style = PolygonSegmentationTool(self.visualizer_page.viewer)
    #             interactor.SetInteractorStyle(self.polygon_interactor_style)
    #             self.polygon_interactor_style.On()
    #             interactor.Render()
    #             print('rendred.')
    #         else:
    #             print('in else')
    #             if hasattr(self, 'polygon_interactor_style'):
    #                 self.polygon_interactor_style.Off()
    #             self.visualizer_page.interactor_style = AbstractInteractorStyle(self.visualizer_page.viewer)
    #             interactor.SetInteractorStyle(self.visualizer_page.interactor_style)
    #             interactor.Render()
