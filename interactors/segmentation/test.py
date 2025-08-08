import vtkmodules.all as vtk
from interactors.abstract_interactor_style import AbstractInteractorStyle


class PolygonSegmentationTool(AbstractInteractorStyle):
    def __init__(self, image_viewer, on_polygon_finished=None):
        super().__init__(image_viewer)
        self.image_renderer = image_viewer.renderer
        self.image_interactor = image_viewer.image_interactor
        self.on_polygon_finished = on_polygon_finished

        self.contour_widget = None
        self.polygon_actor = None
        self.is_finished = False
        self.points = []

        self._setup_widget()

    def _setup_widget(self):
        self.contour_widget = vtk.vtkContourWidget()
        self.contour_widget.SetInteractor(self.image_interactor)
        self.contour_widget.SetRepresentation(vtk.vtkOrientedGlyphContourRepresentation())
        self.contour_widget.SetEnabled(1)
        self.contour_widget.On()

        self.contour_widget.AddObserver(vtk.vtkCommand.EndInteractionEvent, self._on_end_interaction)

    def _on_end_interaction(self, obj, event):
        rep = self.contour_widget.GetRepresentation()
        if hasattr(rep, 'GetClosedLoop') and rep.GetClosedLoop():
            self.points = self.get_polygon_points()
            self.is_finished = True
            self.draw_polygon()
            if self.on_polygon_finished:
                self.on_polygon_finished(self.points)

    def get_polygon_points(self):
        rep = self.contour_widget.GetRepresentation()
        n = rep.GetNumberOfNodes()
        points = []
        for i in range(n):
            p = [0, 0, 0]
            rep.GetNthNodeWorldPosition(i, p)
            points.append(tuple(p))
        return points

    def draw_polygon(self):
        if self.polygon_actor:
            self.image_renderer.RemoveActor(self.polygon_actor)
            self.polygon_actor = None

        if len(self.points) < 2:
            return

        # ساخت ساختار رسم
        vtk_points = vtk.vtkPoints()
        for px, py, *_ in self.points:
            vtk_points.InsertNextPoint(px, py, 0)

        lines = vtk.vtkCellArray()
        for i in range(len(self.points) - 1):
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, i)
            line.GetPointIds().SetId(1, i + 1)
            lines.InsertNextCell(line)

        if self.is_finished and len(self.points) > 2:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, len(self.points) - 1)
            line.GetPointIds().SetId(1, 0)

            lines.InsertNextCell(line)

        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(vtk_points)
        poly_data.SetLines(lines)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly_data)

        # self.polygon_actor = vtk.vtkActor()
        # self.polygon_actor.SetMapper(mapper)
        # self.polygon_actor.GetProperty().SetColor(1, 0.2, 0.2)
        # self.polygon_actor.GetProperty().SetLineWidth(3)
        # self.image_renderer.AddActor(self.polygon_actor)
        # self.image_renderer.Render()

    def reset(self):
        if self.contour_widget:
            self.contour_widget.Initialize()
            self.contour_widget.Render()
        self.points = []
        self.is_finished = False
        if self.polygon_actor:
            self.image_renderer.RemoveActor(self.polygon_actor)
            self.polygon_actor = None
            self.image_renderer.Render()

    def On(self):
        if self.contour_widget:
            self.contour_widget.On()

    def Off(self):
        if self.contour_widget:
            self.contour_widget.Off()
