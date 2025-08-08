from vtkmodules.all import vtkInteractorStyleImage
from PySide6.QtCore import QObject, Signal


class InteractionSignal(QObject):
    interactionOccurred = Signal()


class AbstractInteractorStyle(vtkInteractorStyleImage):
    def __init__(self, image_viewer):
        self.image_viewer = image_viewer
        self.image_renderer = image_viewer.renderer
        # self.interactor = image_viewer.interactor
        super().__init__()
        # left click
        self.AddObserver("LeftButtonPressEvent", self.on_left_button_press)
        self.AddObserver("LeftButtonReleaseEvent", self.on_left_button_release)

        # right click
        self.AddObserver("RightButtonPressEvent", self.on_right_button_press)
        self.AddObserver("RightButtonReleaseEvent", self.on_right_button_release)

        # middle mouse click
        self.AddObserver("MiddleButtonPressEvent", self.on_middle_button_press)
        self.AddObserver("MiddleButtonReleaseEvent", self.on_middle_button_release)

        # moving mouse
        self.AddObserver("MouseMoveEvent", self.on_mouse_move)

        self.left_button_down = False
        self.right_button_down = False
        self.middle_button_down = False
        self.pan_active = False
        self.last_pos = None
        self.widgets_by_slice = {} # widgets on per slice.

    def update_slice(self):
        """
        Update the visibility of measurements when the slice changes.
        """
        current_slice = self.image_viewer.GetSlice()
        print(f"Updating ruler visibility for slice: {current_slice}")

        # Show/hide widgets based on slice
        # widgets = self.widgets_by_slice.values()

        for slice, widgets in self.widgets_by_slice.items():
            if slice == current_slice:
                for widget in widgets:
                    if hasattr(widget, 'measurement_slice'):
                        widget.On()
            else:
                for widget in widgets:
                    if hasattr(widget, 'measurement_slice'):
                        widget.Off()

        # Render to update the display
        self.image_viewer.GetRenderWindow().Render()

    def on_left_button_press(self, obj, event):
        self.left_button_down = True
        self.last_pos = self.GetInteractor().GetEventPosition()
        self.check_left_right_pan_start()

    def on_left_button_release(self, obj, event):
        self.left_button_down = False
        self.last_pos = None
        self.check_left_right_pan_end()


    def on_right_button_press(self, obj, event):
        self.image_viewer.flag_set_custom_window_level = True  # default window width/center are inactive.

        self.right_button_down = True
        self.last_pos = self.GetInteractor().GetEventPosition()
        self.check_left_right_pan_start()

    def on_right_button_release(self, obj, event):
        self.right_button_down = False
        self.last_pos = None
        self.check_left_right_pan_end()

    def on_middle_button_press(self, obj, event):
        self.middle_button_down = True
        self.last_pos = self.GetInteractor().GetEventPosition()

    def on_middle_button_release(self, obj, event):
        self.middle_button_down = False
        self.last_pos = None

    def on_mouse_move(self, obj, event):
        if self.pan_active:  # if left and right click pressed
            super().OnMouseMove()

        elif self.left_button_down:
            self.change_slice_with_left_click()

        elif self.right_button_down:  # if right-click hold: change window level
            self.change_window_level_with_right_click()

        elif self.middle_button_down:  # if middle button hold: zoom in/out
            self.change_zoom_with_middle_button()

    def check_left_right_pan_start(self):
        if self.left_button_down and self.right_button_down:
            # start pan
            self.pan_active = True
            super().OnMiddleButtonDown()

    def check_left_right_pan_end(self):
        # release pan
        if self.pan_active:
            self.pan_active = False
            self.left_button_down = False
            self.right_button_down = False
            super().OnMiddleButtonUp()

    def change_slice_with_left_click(self):
        current_pos = self.GetInteractor().GetEventPosition()
        dy = current_pos[1] - self.last_pos[1]
        basis_slice_change = 5  # each 5 pixel on window

        if abs(dy) >= basis_slice_change:  # Slice change criteria
            # step = 1 if dy > 0 else -1 if dy < 0 else 0  # determine increase/decrease slice
            step = round(dy / basis_slice_change)  # determine increase/decrease slice

            next_slice = self.image_viewer.GetSlice() + step
            max_slice = self.image_viewer.get_count_of_slices()

            if 0 <= next_slice < max_slice:  # if slice valid
                self.image_viewer.SetSlice(next_slice)

            self.image_viewer.Render()
            self.last_pos = current_pos

    def change_window_level_with_right_click(self):
        current_pos = self.GetInteractor().GetEventPosition()
        dx = current_pos[0] - self.last_pos[0]
        dy = current_pos[1] - self.last_pos[1]

        window, level = self.image_viewer.get_window_level()
        # print('current_pos:', current_pos, 'dy:', dy, 'dx:', dx)

        # invert dy for invert change window width
        # if you down your mouse, window width increases
        dy = -dy
        new_y = dy * 1.3
        new_window_center = level + new_y  # level

        # 1.5 is correlation
        new_x = dx * 1.5
        new_window_width = window + new_x

        self.image_viewer.set_window_level(new_window_width, new_window_center)
        self.image_viewer.Render()

        self.last_pos = current_pos

    def change_zoom_with_middle_button(self):
        current_pos = self.GetInteractor().GetEventPosition()
        dy = current_pos[1] - self.last_pos[1]

        camera = self.image_viewer.GetRenderer().GetActiveCamera()
        zoom_factor = 1.0
        zoom_sensitivity = 0.005  # sensitive zoom

        if dy > 0:  # mouse moves up -> zoom in
            zoom_factor = 1 + abs(dy) * zoom_sensitivity
        elif dy < 0:  # mouse moves down -> zoom out
            zoom_factor = 1 / (1 + abs(dy) * zoom_sensitivity)

        camera.Zoom(zoom_factor)
        self.image_viewer.Render()

        self.last_pos = current_pos

    def set_slicer_from_ui(self, slicer):
        self.slicer = slicer
