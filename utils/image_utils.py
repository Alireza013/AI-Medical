import SimpleITK as sitk
import vtkmodules.all as vtk
from vtkmodules.util import numpy_support


def get_orientation_label(direction_cosines: tuple):
    orientation = []
    abs_of_orie = [abs(ele) for ele in direction_cosines]
    max_index = abs_of_orie.index(max(abs_of_orie))
    if max_index == 0:
        orientation.append('R' if direction_cosines[max_index] > 0 else 'L')
    elif max_index == 1:
        orientation.append('A' if direction_cosines[max_index] > 0 else 'P')
    elif max_index == 2:
        orientation.append('I' if direction_cosines[max_index] > 0 else 'S')
    return ''.join(orientation)


def determine_orientation(itk_image: sitk.Image):
    direction = itk_image.GetDirection()
    x_dir = (direction[0], direction[3], direction[6])
    y_dir = (direction[1], direction[4], direction[7])
    z_dir = (direction[2], direction[5], direction[8])
    return get_orientation_label(x_dir) + get_orientation_label(y_dir) + get_orientation_label(z_dir)


def convert_itk2vtk(itk_image: sitk.Image) -> tuple:
    dims = itk_image.GetSize()
    spacing = itk_image.GetSpacing()
    origin = itk_image.GetOrigin()

    image_array = sitk.GetArrayFromImage(itk_image)
    vtk_array = numpy_support.numpy_to_vtk(image_array.ravel(order='C'), deep=True, array_type=vtk.VTK_FLOAT)

    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(dims)
    vtk_image.SetSpacing(spacing)
    vtk_image.SetOrigin(origin)
    vtk_image.GetPointData().SetScalars(vtk_array)

    orientation = determine_orientation(itk_image)
    return vtk_image, orientation
