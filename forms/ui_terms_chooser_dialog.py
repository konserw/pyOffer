# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TermsChooserDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1

from PySide2.QtCore import QMetaObject, Qt
from PySide2.QtWidgets import *


class Ui_TermsChooserDialog(object):
    def setupUi(self, TermsChooserDialog):
        if TermsChooserDialog.objectName():
            TermsChooserDialog.setObjectName(u"TermsChooserDialog")
        TermsChooserDialog.resize(675, 383)
        TermsChooserDialog.setWindowTitle(u"Terms Chooser")
        self.gridLayout = QGridLayout(TermsChooserDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.listView = QListView(TermsChooserDialog)
        self.listView.setObjectName(u"listView")

        self.gridLayout.addWidget(self.listView, 0, 0, 3, 1)

        self.plainTextEdit = QPlainTextEdit(TermsChooserDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setUndoRedoEnabled(False)
        self.plainTextEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.plainTextEdit, 0, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 135, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(TermsChooserDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)


        self.buttonBox.accepted.connect(TermsChooserDialog.accept)
        self.buttonBox.rejected.connect(TermsChooserDialog.reject)

        QMetaObject.connectSlotsByName(TermsChooserDialog)

