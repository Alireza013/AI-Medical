import vtkmodules.all as vtk
from interactors.abstract_interactor_style import AbstractInteractorStyle


class ContourWidget(vtk.vtkContourWidget):
    """
    Customized version of vtkContourWidget.
    some default behaivor has been removed in favor of more user friendly-ness
    """

    def __init__(self, image_viewer):
        super(ContourWidget, self).__init__()
        self.repr = vtk.vtkOrientedGlyphContourRepresentation()
        self.repr.GetLinesProperty().SetLineWidth(2)
        # self.repr.AlwaysOnTopOn()

        self.SetRepresentation(self.repr)
        self.SetInteractor(image_viewer.image_interactor)  # get interactor from image_viewer
        self.SetModeToPolygon()

        interpolator = vtk.vtkLinearContourLineInterpolator()
        self.repr.SetLineInterpolator(interpolator)

        ###
        placer = vtk.vtkImageActorPointPlacer()
        placer.SetImageActor(image_viewer.GetImageActor())  # get actor from image_viewer
        self.repr.SetPointPlacer(placer)
        ###

        self.closed = False
        self.ClosedForFirstTimeEvent = vtk.vtkCommand.UserEvent + 1
        self.AddObserver(vtk.vtkCommand.EndInteractionEvent, self.OnEndInteraction)

    def OnEndInteraction(self, obj, event, calldata=None):
        if obj.repr.GetClosedLoop() and not self.closed:
            self.closed = True
            self.InvokeEvent(self.ClosedForFirstTimeEvent)

    def SetModeToPolygon(self):
        self.FollowCursorOn()
        self.ContinuousDrawOff()
        self.SetAllowNodePicking(False)


class PolygonSegmentationTool(AbstractInteractorStyle):
    def __init__(self, image_viewer, on_polygon_finished=None):
        super().__init__(image_viewer)
        self.active_widget = self.create_contour_widget()
        self.active_widget.Off()
        self.active_contours = []

    def On(self):  # ON
        self.active_widget.On()

    def Off(self):  # OFF
        self.active_widget.Off()

    def create_contour_widget(self):
        widget = ContourWidget(self.image_viewer)
        # placer = vtk.vtkImageActorPointPlacer()
        # placer.SetImageActor(self.image_viewer.GetImageActor())
        # widget.repr.SetPointPlacer(placer)

        widget.AddObserver(widget.ClosedForFirstTimeEvent, self.on_contour_closed)
        widget.AddObserver(vtk.vtkCommand.StartInteractionEvent, self.on_interaction_start)
        widget.On()
        return widget

    def on_contour_closed(self, obj: ContourWidget, event, calldata=None):
        self.active_widget = self.create_contour_widget()
        self.active_contours.append(obj)

    def on_interaction_start(self, obj: ContourWidget, event, calldata=None):
        self.image_viewer.GetMeasurements().AddItem(obj)
