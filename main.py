import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import vtkmodules.vtkCommonCore as vtkCommonCore


if __name__ == "__main__":
    vtkCommonCore.vtkObject.GlobalWarningDisplayOff()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
