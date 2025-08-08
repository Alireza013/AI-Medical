import enum
import vtkmodules.all as vtk


class ViewerType(enum.Enum):
    AXIAL = "Axial"
    SAGITTAL = "Sagittal"
    CORONAL = "Coronal"


class ImageReslice(vtk.vtkImageReslice):  # for set orientation and return image as 2D or 3D
    def __init__(self, vtk_image_data: vtk.vtkImageData, metadata):
        super().__init__()
        self.vtk_image_data = vtk_image_data
        self.metadata = metadata
        self.SetInputData(self.vtk_image_data)
        self.SetOutputDimensionality(3)  # output is 3d image
        self.SetResliceAxesDirectionCosines(1, 0, 0, 0, -1, 0, 0, 0, 1)  # Roll 180 degrees (RAI)

        self.apply_orientation()
        self.Update()

    def apply_orientation(self):
        orientation = self.metadata['orientation']
        print('orientation:', orientation)
        pass


class ImageViewer2D(vtk.vtkResliceImageViewer):
    def __init__(self, render_window: vtk.vtkRenderWindow,
                interactor: vtk.vtkRenderWindowInteractor,
                vtk_image_data: vtk.vtkImageData,
                metadata: dict):
        super().__init__()
        self.viewer_type = None
        self.flag_set_custom_window_level: bool = False

        self.image_render_window: vtk.vtkRenderWindow = render_window
        self.image_interactor: vtk.vtkRenderWindowInteractor = interactor

        self.renderer: vtk.vtkRenderer = self.GetRenderer()
        self.vtk_image_data = vtk_image_data
        self.metadata = metadata

        self.SetRenderWindow(self.image_render_window)
        self.SetupInteractor(self.image_interactor)
        self.renderer.SetBackground(0, 0, 0)

        self.image_reslice = ImageReslice(vtk_image_data, metadata)
        self.SetInputData(self.image_reslice.GetOutput())  # without color map (window level)

        # self.apply_window_level()
        self.UpdateDisplayExtent()
        self.Render()

        self.zoom_to_fit()
        '''
        AXIAL = "Axial"
        SAGITTAL = "Sagittal"
        CORONAL = "Coronal"
        '''

    def set_slice(self, slice_index):
        if not self.flag_set_custom_window_level:
            # if user doesn't work with right click for change window width/center
            self.apply_default_window_level(slice_index)

        self.SetSlice(slice_index)
        self.Render()

    def set_viewer_type(self, viewer_type):
        self.viewer_type = viewer_type

        if viewer_type == ViewerType.AXIAL.name.capitalize():
            self.SetSliceOrientationToXY()
        elif viewer_type == ViewerType.SAGITTAL.name.capitalize():
            self.SetSliceOrientationToYZ()
        elif viewer_type == ViewerType.CORONAL.name.capitalize():
            self.SetSliceOrientationToXZ()
        self.Render()

    def apply_default_window_level(self, slice_index):
        # get window width and window center from lst_windows_levels
        # belongs to the slice[index]

        window_level = self.metadata['windows_levels'][slice_index]
        window_width = window_level['window_width']  # width
        window_center = window_level['window_center']  # level

        print(f'slice: {slice_index}\t width: {window_width}\t center: {window_center}')
        self.set_window_level(window_width, window_center, flag_default=True)

    def set_window_level(self, window_width, window_center, flag_default=False):
        self.SetColorWindow(window_width)

        if flag_default is True:
            self.SetColorLevel(window_center / 2.0)
        else:
            self.SetColorLevel(window_center)

    def get_window_level(self):
        window_width = self.GetColorWindow()
        window_center = self.GetColorLevel()
        # print('window_center:', window_center)

        return window_width, window_center

    def get_count_of_slices(self):
        self.vtk_image_data: vtk.vtkImageData
        dims = self.vtk_image_data.GetDimensions()  # (dimX, dimY, dimZ)
        return dims[2]

    def reset_image_viewer(self, vtk_image_data, metadata):
        del self.image_reslice
        self.image_reslice = ImageReslice(vtk_image_data, metadata)
        self.SetInputData(self.image_reslice.GetOutput())
        self.flag_set_custom_window_level = False

        self.UpdateDisplayExtent()
        self.Render()
        self.zoom_to_fit()

    def zoom_to_fit(self):
        try:
            self.renderer.ResetCamera()
            camera = self.renderer.GetActiveCamera()

            # sure from image is 2d
            camera.ParallelProjectionOn()

            dims = self.vtk_image_data.GetDimensions()
            image_width, image_height = dims[0], dims[1]

            window_size = self.image_render_window.GetSize()
            window_width, window_height = window_size[0], window_size[1]

            spacing = self.vtk_image_data.GetSpacing()

            physical_width = image_width * spacing[0]
            physical_height = image_height * spacing[1]

            image_aspect = physical_width / physical_height
            window_aspect = window_width / window_height

            zoom_factor = 1.0  # lower: zoom in

            if image_aspect > window_aspect:
                # image is wider
                new_scale = (physical_width / 2.0) / (window_width / window_height) * zoom_factor
            else:
                # image is taller
                new_scale = (physical_height / 2.0) * zoom_factor

            camera.SetParallelScale(new_scale)
            self.Render()
            return True

        except Exception as e:
            print(f"Error in zoom_to_fit: {e}")
            return False

