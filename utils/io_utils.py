import pydicom
import SimpleITK as sitk
import vtkmodules.all as vtk
from .image_utils import convert_itk2vtk


def get_window_level_from_dicom(file):
    """Safely read window level from a DICOM file."""
    try:
        meta_dicom = pydicom.dcmread(file)
        window_center = float(meta_dicom.WindowCenter)
        window_width = float(meta_dicom.WindowWidth)
        return {'window_center': window_center, 'window_width': window_width}
    except (FileNotFoundError, AttributeError, ValueError) as e:
        print(f"Could not read DICOM metadata from {file}: {e}")
        return None


def read_nifti(path) -> vtk.vtkImageData:
    """Reads a NIfTI series from a folder and extracts metadata."""
    itk_image = sitk.ReadImage(path)
    vtk_image, _ = convert_itk2vtk(itk_image=itk_image)
    return vtk_image


def read_dicom_folder(folder_path):
    """Reads a DICOM series from a folder and extracts metadata."""
    if not os.path.isdir(folder_path):
        print(f"Error: Directory not found at {folder_path}")
        return None, None

    try:
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(folder_path)
        if not dicom_names:
            print(f"No DICOM files found in {folder_path}")
            return None, None
        reader.SetFileNames(dicom_names)
        itk_image: sitk.Image = reader.Execute()

        lst_windows_levels = []
        for slice_file in dicom_names:
            window_level = get_window_level_from_dicom(slice_file)
            if window_level:
                lst_windows_levels.append(window_level)

        metadata = {'windows_levels': lst_windows_levels}
        vtk_image_data, metadata['orientation'] = convert_itk2vtk(itk_image)

        return vtk_image_data, metadata

    except Exception as e:
        print(f"An error occurred while reading DICOM folder: {e}")
        return None, None
