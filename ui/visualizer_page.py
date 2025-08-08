import os
os.environ["VTK_OPENGL_HYBRID"] = "1"  # Software rendering fallback

from utils import read_dicom_folder
from viewers.viewer_2d import ImageViewer2D
from PySide6.QtCore import Signal
import vtkmodules.all as vtk
from PySide6.QtWidgets import QWidget, QVBoxLayout
from interactors.abstract_interactor_style import AbstractInteractorStyle
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class VisualizerPage(QWidget):
    # Define a signal that will carry the metadata (dict) and image data
    image_loaded = Signal(dict, vtk.vtkImageData)
    
    def __init__(self, parent=None, import_folder_path=None):
        super().__init__(parent)
        self.import_folder_path = import_folder_path
        self.viewer = None
        self.interactor_style = None

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.main_layout.addWidget(self.vtk_widget)

        self.render_window = self.vtk_widget.GetRenderWindow()
        self.image_interactor = self.render_window.GetInteractor()

        if self.import_folder_path:
            self.load_image(self.import_folder_path)

    def load_image(self, folder_path):
        self.import_folder_path = folder_path
        vtk_image_data, metadata = read_dicom_folder(self.import_folder_path)

        if vtk_image_data and metadata:
            self.viewer = ImageViewer2D(self.render_window, self.image_interactor, vtk_image_data, metadata)
            self.viewer.set_viewer_type('Axial')
            
            middle_slice = self.viewer.get_count_of_slices() // 2
            self.viewer.set_slice(middle_slice)
            
            self.interactor_style = AbstractInteractorStyle(self.viewer)
            self.image_interactor.SetInteractorStyle(self.interactor_style)
            self.image_interactor.Initialize()
            self.render_window.Render()
        else:
            print("Failed to load image data.")

    def set_slice(self, slice_index):
        if self.viewer:
            self.viewer.set_slice(slice_index)

    def set_slicer(self, slicer):
        if self.interactor_style:
            self.interactor_style.set_slicer_from_ui(slicer)

    def get_count_of_slices(self):
        if self.viewer:
            return self.viewer.get_count_of_slices()
        return 0
