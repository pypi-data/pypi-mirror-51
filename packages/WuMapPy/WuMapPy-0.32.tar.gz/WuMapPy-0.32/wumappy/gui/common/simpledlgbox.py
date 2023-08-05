# -*- coding: utf-8 -*-
'''
    wumappy.gui.common.simpledlgbox
    -------------------------------

    Simple common dialog box management.

    :copyright: Copyright 2014-2019 Lionel Darras, Philippe Marty, Quentin Vitale and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''
from __future__ import absolute_import
import os
import numpy as np

#from Qt import QtCore, QtWidgets # Qt.py is a shim around all Qt bindings
#from Qt import __binding__
from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *


#---------------------------------------------------------------------------#
# Display Simple Dialog Box Object                                          #
#---------------------------------------------------------------------------#
class Item():
    id = None       # item identifiant
    type = None     # item type, 'CheckBox', 'ComboBox', 'SpinBox', 'DoubleSpinBox', 'Label', 'ValidButton', 'CancelButton', 'MiscButton', ...
    init = None     # item init() function
    update = None   # item update() function
    

class SimpleDlgBox(QDialog):
    
    def __init__(self, title, parent, it_list):
        '''
        Parameters :
        :title: title of dialog box
        :parent: parent windows object
        :it_list: list of items to add in the dialog box.
            [type, label, col_index, isavailable, init, update],... , with :
            :type: item type, 'CheckBox', 'ComboBox', 'SpinBox', 'Label', 'DoubleSpinBox', 'Slider', 'Carto', 'ValidButton', 'CancelButton', 'MiscButton', ...
            :label: item label.
            :col_index: index of the column to display item, 0,1, ...
            :isavailable: True if item is available, False if not.
            :init: initialisation function for item init(), 'None' if no function.
            :update: update function for item update(), 'None' if no function.
        '''
        super(SimpleDlgBox, self).__init__()

        self.asciiset = parent.asciiset
        self.icon = parent.icon
        self.items_list = []

        self.setWindowTitle(title)                  # sets the windows title
        self.setWindowIcon(self.icon)               # sets the window icon
        self.setFont(self.asciiset.font)

        self.layout = QGridLayout()           # builds the main layout
                                                    # the main layout will be composed by layouts as columns
        self.fields_layout = QVBoxLayout()
        self.layout.addLayout(self.fields_layout, 0, 0)

        for it in it_list:
            item = Item()
            item.type = it[0]
            label = self.asciiset.getStringValue(it[1])
            col_index = it[2]
            isavailable = it[3]
            item.init = it[4]
            item.update = it[5]

            isValid = True
            if (item.type == 'CheckBox'):
                item.id = QCheckBox(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'ComboBox'):
                item.id = QComboBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'SpinBox'):
                item.id = QSpinBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'DoubleSpinBox'):
                item.id = QDoubleSpinBox()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Slider'):
                item.id = QSlider()
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Label'):
                item.id = QLabel(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'Image'):
                item.id = QLabel(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'ValidButton'):
                item.id = QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'CancelButton'):
                item.id = QPushButton(label)
                item.id.setFont(self.asciiset.font)
            elif (item.type == 'MiscButton'):
                item.id = QPushButton("")
                item.id.setFont(self.asciiset.font)
            else:
                isValid = False

            if (isValid == True):
                self.items_list.append(item)

                if (item.init != None):                    
                    item.id = item.init(item.id)

                if (item.type == 'CheckBox'):
                    if (item.update != None):
                        item.id.stateChanged.connect(item.update)
                elif (item.type == 'ComboBox'):
                    if (item.update != None):
                        item.id.currentIndexChanged.connect(item.update)
                elif (item.type == 'SpinBox'):
                    if (item.update != None):
                        item.id.valueChanged.connect(item.update)
                elif (item.type == 'DoubleSpinBox'):
                    if (item.update != None):
                        item.id.valueChanged.connect(item.update)
                elif (item.type == 'Slider'):
                    if (item.update != None):
                        item.id.sliderReleased.connect(item.update)
                elif (item.type == 'ValidButton'):
                    item.id.clicked.connect(self.valid)
                elif (item.type == 'CancelButton'):
                    item.id.clicked.connect(self.cancel)
                elif (item.type == 'MiscButton'):
                    if (item.update != None):
                        item.id.clicked.connect(item.update)                    

                self.fields_layout.addWidget(item.id)

        self.setLayout(self.layout)



    def setValidButtonEnabled(self, enabled):
        '''
        Parameters:
        :enabled: True to enable valid button, False if not.
        '''
        self.okbuttonid.setEnabled(enabled)


    def valid(self):
        '''
        Closes the dialog box
        '''
        self.accept()
        self.close()        


    def cancel(self):
        '''
        Closes the dialog box
        '''
        self.close()
