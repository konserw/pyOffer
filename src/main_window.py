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
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow, QDialog

from forms.ui_mainwindow import Ui_MainWindow
from src.customer import CustomerFactory
from src.merchandise import create_merchandise_selection_dialog
from src.offer import Offer
from src.terms import TermsChooserDialog, TermType


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_offer_ui_enabled(False)

        self.offer = None
        self.user = user

        self.ui.action_new.triggered.connect(self.new_offer)
        self.ui.action_new_number.triggered.connect(self.new_offer_symbol)

        self.customer_factory = CustomerFactory(self)

        self.ui.push_button_add_merchandise.clicked.connect(self.select_merchandise)
        self.ui.command_link_button_cutomer.clicked.connect(self.select_customer)

        self.ui.command_link_button_delivery.clicked.connect(self.select_delivery_terms)
        self.ui.command_link_button_offer.clicked.connect(self.select_offer_terms)
        self.ui.command_link_button_billing.clicked.connect(self.select_billing_terms)
        self.ui.command_link_button_delivery_date.clicked.connect(self.select_delivery_date_terms)
        self.ui.plain_text_edit_remarks.textChanged.connect(self.update_remarks)

    def set_offer_ui_enabled(self, enable):
        # menus
        self.ui.menu_export.setEnabled(enable)
        self.ui.action_save.setEnabled(enable)
        self.ui.action_new_number.setEnabled(enable)
        # tabs
        self.ui.tab.setEnabled(enable)
        self.ui.tab_2.setEnabled(enable)

    @Slot()
    def new_offer(self):
        self.offer = Offer.create_empty(self.user, self)
        self.set_offer_ui_enabled(True)
        self.setWindowTitle(f"pyOffer - {self.offer.symbol}")
        self.ui.tableView.setModel(self.offer.merchandise_list)

    @Slot()
    def new_offer_symbol(self):
        self.offer.new_symbol()
        self.setWindowTitle(f"pyOffer - {self.offer.symbol}")

    @Slot()
    def select_customer(self):
        dialog = self.customer_factory.get_customer_selection()
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_customer.setPlainText(dialog.chosen_item.description)
            self.offer.customer = dialog.chosen_item

    @Slot()
    def update_remarks(self):
        self.offer.remarks = self.ui.plain_text_edit_remarks.toPlainText()

    @Slot()
    def select_delivery_terms(self):
        term_type = TermType.delivery
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_offer_terms(self):
        term_type = TermType.offer
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_offer.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_billing_terms(self):
        term_type = TermType.billing
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_billing.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_delivery_date_terms(self):
        term_type = TermType.delivery_date
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery_date.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_merchandise(self):
        dialog = create_merchandise_selection_dialog(self)
        dialog.exec()
        for item in dialog.selected.values():
            self.offer.merchandise_list.change_item_count(item)
