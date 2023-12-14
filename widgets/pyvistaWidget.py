from typing import Optional
import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import *
import PySide6.QtWidgets
# from pyvistaqt import MainWindow as VistaWindow, QtInteractor

# from pyvistaqt.plotting import global_theme
# from pyvista.plotting import Renderer
# try:
#     from pyvista.plotting.utilities import Scraper
# except ImportError:  # PV < 0.40
#     from pyvista.utilities import Scraper

# import pyvistaqt
# from pyvistaqt import MultiPlotter, BackgroundPlotter, MainWindow as PVMainWindow, QtInteractor
# from pyvistaqt.plotting import Counter, QTimer, QVTKRenderWindowInteractor
# from pyvistaqt.editor import Editor
# from pyvistaqt.dialog import FileDialog
# from pyvistaqt.utils import _setup_application, _create_menu_bar, _check_type

# import numpy as np
# import pyvista as pv

# Setting the Qt bindings for QtPy
import os
os.environ["QT_API"] = "pyside6"


#class PyVistaWidget(QtInteractor):
    # def __init__(self, parent: QWidget, off_screen: Optional[bool] = None,**kwargs):
    #     self._closed = True
    #     self.frame = QFrame(parent)
    #     self.frame.setFrameStyle(QFrame.NoFrame)
    #     vlayout = QVBoxLayout()
    #     super().__init__(parent=self.frame, off_screen=off_screen, **kwargs)

    #     vlayout.addWidget(self)
    #     self.frame.setLayout(vlayout)
    #     parent.layout().addWidget(self.frame)

    
    #def PlotPointCloud(self, plotData):
        #point_cloud = pv.PolyData(plotData)   
        # Make data array using z-component of points array
        # data = plotData[:, -1]

        # point_cloud["elevation"] = data

        # self.add_mesh(point_cloud, point_size=0.1, cmap="jet", render_points_as_spheres=True, lighting = True, smooth_shading=True)
        # self.set_scale(zscale = 200)
        # self.show_grid()
        
        # #self.plotterWindow.show()     

                