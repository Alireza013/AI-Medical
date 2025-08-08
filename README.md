# Medical Imaging Viewer with AI Integration

A PySide6-based Python desktop application and work station for medical image visualization and AI-assisted analysis, supporting DICOM/NIfTI formats.

## Features

- **Multi-View Visualization**
  - Axial, Coronal, Sagittal
  - Real-time slice navigation

- **AI Integration**
  - Training status monitoring
  - Image segmentation tools
  - Diagnostic assistance

- **UI**
  - Dark theme with orange accents
    * Eye-friendly interface for prolonged medical imaging sessions
  - Adaptable Workspace
    * Dockable panels (Left/Right) with persistent user preferences
    * viewport management (axial/sagittal/coronal)

- **File Support**
  - DICOM (.dcm)
  - NIfTI (.nii, .nii.gz)

## Integrated Core Modules

# 1. Visualizer Module (ITK/VTK Engine)
- **2D/3D Rendering**
    * DICOM/NIfTI slice visualization via ITK->VTK pipeline

- **AI Overlays**
    * Real-time segmentation mask

# 2. Image Processing Module
- **Preprocessing Tools**
    * Contrast adjustment
    * Histogram analysis & adaptive equalization

- **CV Operations**
    * Image processing modules for AI preprocess

# 3. AI/NLP Module
- **AI Suite**
    * Segmentation, Classification pipelines

- **Doctor-AI Interaction**
    * Text command processing
    * Structured reporting with auto-generated findings

![Cross-Moudle Workflow](medical_workflow.png)

## Prerequisites

- Python 3.8+
- Required packages:
  ```bash
    pip install PySide6 vtk itk numpy pydicom SimpleITK
  ```

## Installation

# 1. Go to repository:
  ```bash
    cd AI-Medical
  ```
# 2. Install dependencies:
  ```bash
    pip install -r requirements.txt
  ```

## Usage
# Run the main application:
  ```bash
    python main.py
  ```

## Key Controls:

- file > Open: Load medical images

## Project Structure
.
|-- .gitignore
|-- README.md
|-- main.py
|-- requirements.txt
|-- interactors
|   |-- __init__.py
|   `-- abstract_interactor_style.py
|-- segmentation
|   |-- __init__.py
|   `-- polygon_segmentation_tool.py
|-- ui
|   |-- __init__.py
|   |-- main_window.py
|   |-- top_bar.py
|   |-- left_dock.py
|   |-- right_dock.py
|   |-- visualizer_page.py
|   |-- navigation_sidebar.py
|   |-- train_status_page.py
|   |-- image_details_page.py
|   `-- split_viewer_page.py
|-- utils
|   |-- __init__.py
|   |-- image_utils.py
|   `-- io_utils.py
`-- viewers
    |-- __init__.py
    `-- viewer_2d.py

# 1. GUI Components
- **MainWindow.py**
    * Manages window layout/states
    * Coordinates communication between modules

- **TopBar.py**
    * File operations (Open/Save)
    * AI workflow triggers (Train/Inference)

- **LeftDock.py**
    * Image measurement tools
    * Histogram/contrast adjustment panel

- **RightDock.py**
    * AI model selection dropdowns
    * Inference confidence

# 2. AI Components
- **TrainStatusPage.py**
    * Training metrics visualization
    * Model configuration presets

# 3. Visualizer Components
- **VisualizerPage.py**
    * Quad-view layout (axial/sagittal/coronal/3D)
    * VTK-based volume rendering pipeline
    * ITK DICOM/NIfTI reader integration
    * Segmentation overlay

# 4. ImageProcessor Components
- **ImageDetailsPage.py**
    * DICOM metadata browser
    * Pixel statistics analyzer




