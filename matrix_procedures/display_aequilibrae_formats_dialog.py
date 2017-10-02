"""
 -----------------------------------------------------------------------------------------------------------
 Package:    AequilibraE

 Name:       Loads AequilibraE datasets for visualization
 Purpose:    Allows visual inspection of data

 Original Author:  Pedro Camargo (c@margo.co)
 Contributors:
 Last edited by: Pedro Camargo

 Website:    www.AequilibraE.com
 Repository:  https://github.com/AequilibraE/AequilibraE

 Created:    2017-10-02
 Updated:
 Copyright:   (c) AequilibraE authors
 Licence:     See LICENSE.TXT
 -----------------------------------------------------------------------------------------------------------
 """

from PyQt4 import QtGui, uic
from PyQt4.QtGui import *
from ..common_tools import DatabaseModel, NumpyModel
from ..aequilibrae.matrix import AequilibraeMatrix
from ..common_tools.auxiliary_functions import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__),  'forms/ui_data_viewer.ui'))

from PyQt4.QtGui import QHBoxLayout, QTableView, QTableWidget, QPushButton, QVBoxLayout
from PyQt4.QtGui import QComboBox, QCheckBox, QSpinBox, QLabel, QSpacerItem


class DisplayAequilibraEFormatsDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, datasource):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        self.path = standard_path()
        self.error = None
        self.data_path = None
        self.data_to_show = datasource
        if isinstance(datasource, AequilibraeMatrix):
            self.data_type = 'matrix'
        else:
            self.data_type = 'dataset'

    # Elements that will be used during the displaying
        self._layout = QVBoxLayout()
        self.table = QTableView()
        self._layout.addWidget(self.table)

        # Settings for displaying
        self.show_layout = QHBoxLayout()

        # Thousand separator
        self.thousand_separator = QCheckBox()
        self.thousand_separator.setChecked(True)
        self.thousand_separator.setText('Thousands separator')
        self.thousand_separator.toggled.connect(self.format_showing)
        self.show_layout.addWidget(self.thousand_separator)

        self.spacer = QSpacerItem(5, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.show_layout.addItem(self.spacer)

        # Decimals
        txt = QLabel()
        txt.setText('Decimal places')
        self.show_layout.addWidget(txt)
        self.decimals = QSpinBox()
        self.decimals.valueChanged.connect(self.format_showing)
        self.decimals.setMinimum(0)
        self.decimals.setValue(4)
        self.decimals.setMaximum(10)

        self.show_layout.addWidget(self.decimals)
        self._layout.addItem(self.show_layout)

        # differentiates between matrix and dataset
        if self.data_type == 'matrix':
            self.data_to_show.computational_view([self.data_to_show.names[0]])
            # Matrices need cores and indices to be set as well
            self.mat_layout = QHBoxLayout()
            self.mat_list = QComboBox()
            for n in self.data_to_show.names:
                self.mat_list.addItem(n)

            self.mat_list.currentIndexChanged.connect(self.change_matrix_cores)
            self.mat_layout.addWidget(self.mat_list)

            self.idx_list = QComboBox()
            for i in self.data_to_show.index_names:
                self.idx_list.addItem(i)
            self.idx_list.currentIndexChanged.connect(self.change_matrix_cores)
            self.mat_layout.addWidget(self.idx_list)
            self._layout.addItem(self.mat_layout)
            self.change_matrix_cores()

        self.but_close = QPushButton()
        self.but_close.clicked.connect(self.exit_procedure)
        self.but_close.setText('Close')
        self._layout.addWidget(self.but_close)


        # We chose to use QTableView. However, if we want to allow the user to edit the dataset
        # The we need to allow them to switch to the slower QTableWidget
        # Code below

        # self.table = QTableWidget(self.data_to_show.entries, self.data_to_show.num_fields)
        # self.table.setHorizontalHeaderLabels(self.data_to_show.fields)
        # self.table.setObjectName('data_viewer')
        #
        # self.table.setVerticalHeaderLabels([str(x) for x in self.data_to_show.index[:]])
        # self.table.clearContents()
        #
        # for i in range(self.data_to_show.entries):
        #     for j, f in enumerate(self.data_to_show.fields):
        #         item1 = QTableWidgetItem(str(self.data_to_show.data[f][i]))
        #         item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        #         self.table.setItem(i, j, item1)

        self.resize(700, 500)
        self.setLayout(self._layout)
        self.format_showing()

    def format_showing(self):
        decimals = self.decimals.value()
        separator = self.thousand_separator.isChecked()
        if isinstance(self.data_to_show, AequilibraeMatrix):
            m = NumpyModel(self.data_to_show, separator, decimals)
        else:
            m = DatabaseModel(self.data_to_show, separator, decimals)
        self.table.clearSpans()
        self.table.setModel(m)

    def change_matrix_cores(self):
        self.data_to_show.computational_view([self.mat_list.currentText()])
        self.data_to_show.set_index(0)
        self.format_showing()


    def exit_procedure(self):
        self.close()