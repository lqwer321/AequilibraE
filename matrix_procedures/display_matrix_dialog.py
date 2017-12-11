"""
 -----------------------------------------------------------------------------------------------------------
 Package:    AequilibraE

 Name:       Loads Matrix Visualizer
 Purpose:    allowing user to see matrices loaded in AequilibraE format

 Original Author:  Pedro Camargo (c@margo.co)
 Contributors:
 Last edited by: Pedro Camargo

 Website:    www.AequilibraE.com
 Repository:  https://github.com/AequilibraE/AequilibraE

 Created:    2016-10-02
 Updated:
 Copyright:   (c) AequilibraE authors
 Licence:     See LICENSE.TXT
 -----------------------------------------------------------------------------------------------------------
 """

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import uic
from ..common_tools.auxiliary_functions import *
from ..aequilibrae.matrix import AequilibraeMatrix
from ..common_tools.get_output_file_name import GetOutputFileName
from display_aequilibrae_formats_dialog import DisplayAequilibraEFormatsDialog
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__),  'forms/ui_data_viewer.ui'))


class DisplayMatrixDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, **kwargs):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.path = standard_path()
        self.error = None
        self.data_path = None
        self.dataset = AequilibraeMatrix()
        self.but_load.setText('Load matrix')
        self.but_load.clicked.connect(self.load_the_vector)
        self.load_the_vector()

    def load_the_vector(self):
        self.error = None
        self.data_path, _ = GetOutputFileName(self, 'AequilibraE matrix',
                                              ["Aequilibrae matrix(*.aem)"], '.aem', self.path)

        if self.data_path is None:
            self.error = 'Path provided is not a valid matrix'

        if self.error is None:
            try:
                self.but_load.setText('working...')
                self.but_load.setEnabled(False)
                self.dataset.load(self.data_path)
            except:
                self.error = 'Could not load matrix'

        if self.error is None:
            dlg2 = DisplayAequilibraEFormatsDialog(self.iface, self.dataset)
            dlg2.show()
            dlg2.exec_()
            self.exit_procedure()
        else:
            qgis.utils.iface.messageBar().pushMessage("Error:", self.error, level=1)

    def exit_procedure(self):
        self.close()
