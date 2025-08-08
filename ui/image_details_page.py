from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import vtkmodules.all as vtk

class ImageDetailsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        self.layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: black;")

        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        title_label = QLabel("Image Details")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        title_label.setStyleSheet("""
            color: #FF8C00;
            font-size: 18px;
            font-weight: bold;
            padding-bottom: 10px;
        """)
        self.layout.addWidget(title_label)

        no_image_label = QLabel("No image loaded.")
        no_image_label.setStyleSheet("color: #ccc;")
        self.layout.addWidget(no_image_label)

        self.layout.addStretch() # Pushes content to the top

    @Slot(dict, vtk.vtkImageData)
    def update_details(self, metadata, image_data):
        """This is the slot that receives the signal from VisualizerPage."""
        # Clear the existing widgets from the layout
        self.setup_ui()

        self.layout.takeAt(1).widget().setParent(None)
        self.layout.takeAt(1)

        # Add new labels with details from the metadata
        orientation = metadata.get('orientation', 'N/A')
        dims = image_data.GetDimensions()
        slice_count = dims[2]

        orientation_label = QLabel(f"Orientation: {orientation}")
        orientation_label.setStyleSheet("color: #ccc; font-size: 13px;")
        self.layout.addWidget(orientation_label)

        dimensions_label = QLabel(f"Dimensions: {dims[0]} x {dims[1]} x {dims[2]}")
        dimensions_label.setStyleSheet("color: #ccc; font-size: 13px;")
        self.layout.addWidget(dimensions_label)

        slice_count_label = QLabel(f"Slice Count: {slice_count}")
        slice_count_label.setStyleSheet("color: #ccc; font-size: 13px;")
        self.layout.addWidget(slice_count_label)
        
        self.layout.addStretch()