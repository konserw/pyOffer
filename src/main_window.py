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
from __future__ import annotations

from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import QMainWindow, QDialog, QApplication

from forms.ui_mainwindow import Ui_MainWindow
from src.customer import CustomerSelectionDialog
from src.merchandise import MerchandiseSelectionDialog, DiscountDialog
from src.offer import Offer
from src.terms import TermsChooserDialog, TermType
from src.user import User


class MainWindow(QMainWindow):
    def __init__(self, user: User):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_offer_ui_enabled(False)

        self.offer = None
        self.user = user

        self.ui.action_new.triggered.connect(self.new_offer)
        self.ui.action_open.triggered.connect(self.load_offer)
        self.ui.action_save.triggered.connect(self.save_offer)
        self.ui.action_new_number.triggered.connect(self.new_offer_symbol)
        self.ui.action_exit.triggered.connect(self.exit)

        self.ui.action_print.triggered.connect(self.print_preview)
        self.ui.action_PDF.triggered.connect(self.print_pdf)

        self.ui.action_about.triggered.connect(self.about)
        self.ui.action_about_Qt.triggered.connect(self.about_qt)

        self.ui.push_button_add_merchandise.clicked.connect(self.select_merchandise)
        self.ui.push_button_remove_row.clicked.connect(self.remove_row)
        self.ui.push_button_discount.clicked.connect(self.set_discount)

        self.ui.command_link_button_customer.clicked.connect(self.select_customer)
        self.ui.check_box_query_date.stateChanged.connect(self.inquiry_date_toggled)
        self.ui.check_box_query_number.stateChanged.connect(self.inquiry_number_toggled)
        self.ui.line_edit_query_number.textChanged.connect(self.inquiry_number_changed)

        self.ui.command_link_button_delivery.clicked.connect(self.select_delivery_terms)
        self.ui.command_link_button_offer.clicked.connect(self.select_offer_terms)
        self.ui.command_link_button_billing.clicked.connect(self.select_billing_terms)
        self.ui.command_link_button_delivery_date.clicked.connect(self.select_delivery_date_terms)
        self.ui.plain_text_edit_remarks.textChanged.connect(self.update_remarks)

    def set_offer_ui_enabled(self, enable: bool) -> None:
        # menus
        self.ui.menu_export.setEnabled(enable)
        self.ui.action_save.setEnabled(enable)
        self.ui.action_new_number.setEnabled(enable)
        # tabs
        self.ui.tab.setEnabled(enable)
        self.ui.tab_2.setEnabled(enable)

    @Slot()
    def new_offer(self) -> None:
        self.offer = Offer.create_empty(self.user, self)
        self.set_offer_ui_enabled(True)
        self.setWindowTitle(f"pyOffer - {self.offer.symbol}")
        self.ui.tableView.setModel(self.offer.merchandise_list)

    @Slot()
    def new_offer_symbol(self) -> None:
        self.offer.new_symbol()
        self.setWindowTitle(f"pyOffer - {self.offer.symbol}")

    @Slot()
    def select_customer(self) -> None:
        dialog = CustomerSelectionDialog.make(self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_customer:
            self.ui.plain_text_edit_customer.setPlainText(dialog.chosen_customer.description)
            self.offer.customer = dialog.chosen_customer

    @Slot()
    def update_remarks(self) -> None:
        self.offer.remarks = self.ui.plain_text_edit_remarks.toPlainText()

    @Slot()
    def select_delivery_terms(self) -> None:
        term_type = TermType.delivery
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_offer_terms(self) -> None:
        term_type = TermType.offer
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_offer.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_billing_terms(self) -> None:
        term_type = TermType.billing
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_billing.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_delivery_date_terms(self) -> None:
        term_type = TermType.delivery_date
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery_date.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_merchandise(self) -> None:
        dialog = MerchandiseSelectionDialog.make(self)
        dialog.exec()
        for item in dialog.selected.values():
            self.offer.merchandise_list.change_item_count(item)

    @Slot()
    def remove_row(self) -> None:
        index = self.ui.tableView.currentIndex()
        self.offer.merchandise_list.removeRow(index.row())

    @Slot()
    def set_discount(self) -> None:
        dialog = DiscountDialog(self)
        dialog.line_edit_expression.textChanged.connect(self.offer.merchandise_list.highlight_rows)
        self.offer.merchandise_list.highlight_rows("")
        if dialog.exec_() == QDialog.Accepted:
            self.offer.merchandise_list.set_discount(dialog.filter_expression, dialog.discount_value)
        self.offer.merchandise_list.highlight_rows(None)

    @Slot(int)
    def inquiry_date_toggled(self, state: int) -> None:
        enabled = state == Qt.Checked
        self.ui.push_button_query_date.setEnabled(enabled)
#        self.ui.line_edit_query_date
        if not enabled:
            self.offer.inquiry_date = None

    @Slot(int)
    def inquiry_number_toggled(self, state: int) -> None:
        enabled = state == Qt.Checked
        self.ui.line_edit_query_number.setEnabled(enabled)
        if not enabled:
            self.offer.inquiry_number = None

    @Slot(str)
    def inquiry_number_changed(self, text: str) -> None:
        self.offer.inquiry_number = text

    @Slot()
    def load_offer(self) -> None:
        pass

    @Slot()
    def save_offer(self) -> None:
        pass

    @Slot()
    def exit(self) -> None:
        """Forward to QMainWindow.close, but keep here for sake of tests"""
        super().close()

    @Slot()
    def print_preview(self) -> None:
        pass

    @Slot()
    def print_pdf(self) -> None:
        pass

    @Slot()
    def about(self) -> None:
        pass

    @Slot()
    def about_qt(self) -> None:
        """Forward to QApplication.aboutQt, but keep here for sake of tests"""
        QApplication.aboutQt()
