# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
from PySide2.QtWidgets import QMainWindow, QDialog

from forms.ui_mainwindow import Ui_MainWindow
from src.customer import CustomerFactory
from src.merchandise import MerchandiseListModel, create_merchandise_selection_dialog
from src.terms import TermChooserDialogFactory, TermType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.merchandise_list_model = MerchandiseListModel(self)
        self.ui.tableView.setModel(self.merchandise_list_model)
        self.term_chooser_factory = TermChooserDialogFactory(self)
        self.customer_factory = CustomerFactory(self)

        self.ui.push_button_add_merchandise.clicked.connect(self.select_merchandise)
        self.ui.command_link_button_cutomer.clicked.connect(self.select_customer)

        self.ui.command_link_button_delivery.clicked.connect(self.select_delivery_terms)
        self.ui.command_link_button_offer.clicked.connect(self.select_offer_terms)
        self.ui.command_link_button_billing.clicked.connect(self.select_billing_terms)
        self.ui.command_link_button_delivery_date.clicked.connect(self.select_delivery_date_terms)

    def select_customer(self):
        dialog = self.customer_factory.get_customer_selection()
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_customer.setPlainText(dialog.chosen_item.description)

    def select_delivery_terms(self):
        dialog = self.term_chooser_factory.get_terms_chooser_dialog(TermType.delivery)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery.setPlainText(dialog.chosen_item.long_desc)

    def select_offer_terms(self):
        dialog = self.term_chooser_factory.get_terms_chooser_dialog(TermType.offer)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_offer.setPlainText(dialog.chosen_item.long_desc)

    def select_billing_terms(self):
        dialog = self.term_chooser_factory.get_terms_chooser_dialog(TermType.billing)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_billing.setPlainText(dialog.chosen_item.long_desc)

    def select_delivery_date_terms(self):
        dialog = self.term_chooser_factory.get_terms_chooser_dialog(TermType.delivery_date)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery_date.setPlainText(dialog.chosen_item.long_desc)

    def select_merchandise(self):
        dialog = create_merchandise_selection_dialog(self)
        dialog.exec()
        for item in dialog.selected.values():
            self.merchandise_list_model.change_item_count(item)
