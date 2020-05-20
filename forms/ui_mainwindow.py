# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
################################################################################

from PySide2.QtCore import QCoreApplication, QMetaObject, QRect, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *

from src.merchandise import MerchandiseListView
# noinspection PyUnresolvedReferences
import resources.all  # noqa: F401


class Ui_MainWindow(object):
    def __init__(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1134, 1045)
        MainWindow.setWindowTitle(u"pyOffer")
        icon = QIcon()
        icon.addFile(u":/ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.action_new = QAction(MainWindow)
        self.action_new.setObjectName(u"action_new")
        self.action_open = QAction(MainWindow)
        self.action_open.setObjectName(u"action_open")
        self.action_save = QAction(MainWindow)
        self.action_save.setObjectName(u"action_save")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_PDF = QAction(MainWindow)
        self.action_PDF.setObjectName(u"action_PDF")
        self.action_print = QAction(MainWindow)
        self.action_print.setObjectName(u"action_print")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about_Qt = QAction(MainWindow)
        self.action_about_Qt.setObjectName(u"action_about_Qt")
        self.action_new_number = QAction(MainWindow)
        self.action_new_number.setObjectName(u"action_new_number")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralWidget)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.push_button_add_merchandise = QPushButton(self.tab)
        self.push_button_add_merchandise.setObjectName(u"push_button_add_merchandise")

        self.horizontalLayout_2.addWidget(self.push_button_add_merchandise)

        self.push_button_discount = QPushButton(self.tab)
        self.horizontalLayout_2.addWidget(self.push_button_discount)
        self.push_button_discount_group = QPushButton(self.tab)
        self.horizontalLayout_2.addWidget(self.push_button_discount_group)

        self.push_button_remove_row = QPushButton(self.tab)
        self.push_button_remove_row.setObjectName(u"push_button_remove_row")

        self.horizontalLayout_2.addWidget(self.push_button_remove_row)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.tableView = MerchandiseListView(self.tab)
        self.tableView.setObjectName(u"tableView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.tableView)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout = QGridLayout(self.tab_2)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.command_link_button_customer = QCommandLinkButton(self.tab_2)
        self.command_link_button_customer.setObjectName(u"command_link_button_cutomer")

        self.horizontalLayout_3.addWidget(self.command_link_button_customer)

        self.plain_text_edit_customer = QPlainTextEdit(self.tab_2)
        self.plain_text_edit_customer.setObjectName(u"plain_text_edit_customer")
        sizePolicy.setHeightForWidth(self.plain_text_edit_customer.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_customer.setSizePolicy(sizePolicy)
        self.plain_text_edit_customer.setTabChangesFocus(True)
        self.plain_text_edit_customer.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plain_text_edit_customer.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.plain_text_edit_customer)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.grup_box_query = QGroupBox(self.tab_2)
        self.grup_box_query.setObjectName(u"grup_box_query")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.grup_box_query.sizePolicy().hasHeightForWidth())
        self.grup_box_query.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.grup_box_query)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.check_box_query_date = QCheckBox(self.grup_box_query)
        self.check_box_query_date.setObjectName(u"check_box_query_date")

        self.horizontalLayout.addWidget(self.check_box_query_date)

        self.line_edit_query_date = QLineEdit(self.grup_box_query)
        self.line_edit_query_date.setObjectName(u"line_edit_query_date")
        self.line_edit_query_date.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line_edit_query_date.sizePolicy().hasHeightForWidth())
        self.line_edit_query_date.setSizePolicy(sizePolicy2)
        self.line_edit_query_date.setReadOnly(False)

        self.horizontalLayout.addWidget(self.line_edit_query_date)

        self.push_button_query_date = QPushButton(self.grup_box_query)
        self.push_button_query_date.setObjectName(u"push_button_query_date")
        sizePolicy2.setHeightForWidth(self.push_button_query_date.sizePolicy().hasHeightForWidth())
        self.push_button_query_date.setSizePolicy(sizePolicy2)
        icon1 = QIcon()
        icon1.addFile(u":/calendar", QSize(), QIcon.Normal, QIcon.Off)
        self.push_button_query_date.setIcon(icon1)
        self.push_button_query_date.setIconSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.push_button_query_date)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(6)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.check_box_query_number = QCheckBox(self.grup_box_query)
        self.check_box_query_number.setObjectName(u"check_box_query_number")

        self.horizontalLayout_11.addWidget(self.check_box_query_number)

        self.line_edit_query_number = QLineEdit(self.grup_box_query)
        self.line_edit_query_number.setObjectName(u"line_edit_query_number")
        self.line_edit_query_number.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.line_edit_query_number.sizePolicy().hasHeightForWidth())
        self.line_edit_query_number.setSizePolicy(sizePolicy3)
        self.line_edit_query_number.setMinimumSize(QSize(200, 0))
        self.line_edit_query_number.setMaximumSize(QSize(500, 16777215))
        self.line_edit_query_number.setBaseSize(QSize(500, 0))
        self.line_edit_query_number.setReadOnly(False)

        self.horizontalLayout_11.addWidget(self.line_edit_query_number)


        self.verticalLayout.addLayout(self.horizontalLayout_11)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.plain_text_edit_query = QPlainTextEdit(self.grup_box_query)
        self.plain_text_edit_query.setObjectName(u"plain_text_edit_query")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Ignored)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.plain_text_edit_query.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_query.setSizePolicy(sizePolicy4)
        self.plain_text_edit_query.setMaximumSize(QSize(16777215, 16777215))
        self.plain_text_edit_query.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.plain_text_edit_query)


        self.gridLayout.addWidget(self.grup_box_query, 1, 0, 1, 2)

        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setSpacing(6)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.command_link_button_delivery = QCommandLinkButton(self.groupBox)
        self.command_link_button_delivery.setObjectName(u"command_link_button_delivery")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.command_link_button_delivery)

        self.plain_text_edit_delivery = QPlainTextEdit(self.groupBox)
        self.plain_text_edit_delivery.setObjectName(u"plain_text_edit_delivery")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.plain_text_edit_delivery.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_delivery.setSizePolicy(sizePolicy5)
        self.plain_text_edit_delivery.setMaximumSize(QSize(16777215, 16777215))
        self.plain_text_edit_delivery.setUndoRedoEnabled(False)
        self.plain_text_edit_delivery.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.plain_text_edit_delivery)

        self.command_link_button_delivery_date = QCommandLinkButton(self.groupBox)
        self.command_link_button_delivery_date.setObjectName(u"command_link_button_delivery_date")

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.command_link_button_delivery_date)

        self.plain_text_edit_delivery_date = QPlainTextEdit(self.groupBox)
        self.plain_text_edit_delivery_date.setObjectName(u"plain_text_edit_delivery_date")
        sizePolicy5.setHeightForWidth(self.plain_text_edit_delivery_date.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_delivery_date.setSizePolicy(sizePolicy5)
        self.plain_text_edit_delivery_date.setMaximumSize(QSize(16777215, 16777215))
        self.plain_text_edit_delivery_date.setUndoRedoEnabled(False)
        self.plain_text_edit_delivery_date.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.plain_text_edit_delivery_date)

        self.command_link_button_billing = QCommandLinkButton(self.groupBox)
        self.command_link_button_billing.setObjectName(u"command_link_button_billing")

        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.command_link_button_billing)

        self.plain_text_edit_billing = QPlainTextEdit(self.groupBox)
        self.plain_text_edit_billing.setObjectName(u"plain_text_edit_billing")
        sizePolicy5.setHeightForWidth(self.plain_text_edit_billing.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_billing.setSizePolicy(sizePolicy5)
        self.plain_text_edit_billing.setMaximumSize(QSize(16777215, 16777215))
        self.plain_text_edit_billing.setUndoRedoEnabled(False)
        self.plain_text_edit_billing.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.plain_text_edit_billing)

        self.command_link_button_offer = QCommandLinkButton(self.groupBox)
        self.command_link_button_offer.setObjectName(u"command_link_button_offer")

        self.formLayout.setWidget(6, QFormLayout.SpanningRole, self.command_link_button_offer)

        self.plain_text_edit_offer = QPlainTextEdit(self.groupBox)
        self.plain_text_edit_offer.setObjectName(u"plain_text_edit_offer")
        sizePolicy5.setHeightForWidth(self.plain_text_edit_offer.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_offer.setSizePolicy(sizePolicy5)
        self.plain_text_edit_offer.setMaximumSize(QSize(16777215, 16777215))
        self.plain_text_edit_offer.setUndoRedoEnabled(False)
        self.plain_text_edit_offer.setReadOnly(True)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.plain_text_edit_offer)

        self.command_link_button_remarks = QCommandLinkButton(self.groupBox)
        self.command_link_button_remarks.setObjectName(u"command_link_button_remarks")
        self.command_link_button_remarks.setEnabled(False)
        self.command_link_button_remarks.setAutoFillBackground(False)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.command_link_button_remarks)

        self.plain_text_edit_remarks = QPlainTextEdit(self.groupBox)
        self.plain_text_edit_remarks.setObjectName(u"plain_text_edit_remarks")
        sizePolicy5.setHeightForWidth(self.plain_text_edit_remarks.sizePolicy().hasHeightForWidth())
        self.plain_text_edit_remarks.setSizePolicy(sizePolicy5)
        self.plain_text_edit_remarks.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.plain_text_edit_remarks)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(11, QFormLayout.FieldRole, self.verticalSpacer_6)

        self.gridLayout.addWidget(self.groupBox, 2, 0, 2, 2)

#        self.kolumny = QGroupBox(self.tab_2)
#        self.kolumny.setObjectName(u"kolumny")
#        sizePolicy2.setHeightForWidth(self.kolumny.sizePolicy().hasHeightForWidth())
#        self.kolumny.setSizePolicy(sizePolicy2)
#        self.verticalLayout_4 = QVBoxLayout(self.kolumny)
#        self.verticalLayout_4.setSpacing(6)
#        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
#        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
#        self.check_box_no_column = QCheckBox(self.kolumny)
#        self.check_box_no_column.setObjectName(u"check_box_no_column")
#        self.check_box_no_column.setEnabled(False)
#        self.check_box_no_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_no_column)
#
#        self.check_box_merchandise_column = QCheckBox(self.kolumny)
#        self.check_box_merchandise_column.setObjectName(u"check_box_merchandise_column")
#        self.check_box_merchandise_column.setEnabled(False)
#        self.check_box_merchandise_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_merchandise_column)
#
#        self.check_box_details_column = QCheckBox(self.kolumny)
#        self.check_box_details_column.setObjectName(u"check_box_details_column")
#        self.check_box_details_column.setEnabled(True)
#        self.check_box_details_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_details_column)
#
#        self.check_box_list_price_column = QCheckBox(self.kolumny)
#        self.check_box_list_price_column.setObjectName(u"check_box_list_price_column")
#        self.check_box_list_price_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_list_price_column)
#
#        self.check_box_discount_column = QCheckBox(self.kolumny)
#        self.check_box_discount_column.setObjectName(u"check_box_discount_column")
#        self.check_box_discount_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_discount_column)
#
#        self.check_box_price_column = QCheckBox(self.kolumny)
#        self.check_box_price_column.setObjectName(u"check_box_price_column")
#        self.check_box_price_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_price_column)
#
#        self.check_box_quantity_column = QCheckBox(self.kolumny)
#        self.check_box_quantity_column.setObjectName(u"check_box_quantity_column")
#        self.check_box_quantity_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_quantity_column)
#
#        self.check_box_total_column = QCheckBox(self.kolumny)
#        self.check_box_total_column.setObjectName(u"check_box_total_column")
#        self.check_box_total_column.setEnabled(False)
#        self.check_box_total_column.setChecked(True)
#
#        self.verticalLayout_4.addWidget(self.check_box_total_column)
#
#        self.gridLayout.addWidget(self.kolumny, 2, 2, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 430, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 3, 2, 2, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1134, 24))
        self.menu_offer = QMenu(self.menuBar)
        self.menu_offer.setObjectName(u"menu_offer")
        self.menu_export = QMenu(self.menuBar)
        self.menu_export.setObjectName(u"menu_export")
        self.menu_help = QMenu(self.menuBar)
        self.menu_help.setObjectName(u"menu_help")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menu_offer.menuAction())
        self.menuBar.addAction(self.menu_export.menuAction())
        self.menuBar.addAction(self.menu_help.menuAction())
        self.menu_offer.addAction(self.action_new)
        self.menu_offer.addAction(self.action_open)
        self.menu_offer.addAction(self.action_save)
        self.menu_offer.addAction(self.action_new_number)
        self.menu_offer.addAction(self.action_exit)
        self.menu_export.addAction(self.action_PDF)
        self.menu_export.addAction(self.action_print)
        self.menu_help.addAction(self.action_about)
        self.menu_help.addAction(self.action_about_Qt)

        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
