"""
 -----------------------------------------------------------------------------------------------------------
 Package:    AequilibraE

 Name:       Applying Gravity model
 Purpose:    Applies synthetic gravity model

 Original Author:  Pedro Camargo (c@margo.co)
 Contributors:
 Last edited by: Pedro Camargo

 Website:    www.AequilibraE.com
 Repository:  https://github.com/AequilibraE/AequilibraE

 Created:    2016-10-03
 Updated:
 Copyright:   (c) AequilibraE authors
 Licence:     See LICENSE.TXT
 -----------------------------------------------------------------------------------------------------------
 """

from qgis.core import *
from PyQt4.QtCore import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from ..common_tools import WorkerThread
from aequilibrae.distribution import GravityApplication

class ApplyGravityProcedure(WorkerThread):
    def __init__(self, parentThread,  impedance, rows, columns, model):
        WorkerThread.__init__(self, parentThread)
        self.gravity = GravityApplication(rows, columns, impedance, model)
        self.error = None

    def doWork(self):
        self.gravity.apply()
        self.emit(SIGNAL("finished_threaded_procedure( PyQt_PyObject )"),0)

if __name__ == '__main__':
    main()
