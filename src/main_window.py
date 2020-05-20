# pyOffer - program for creating business proposals for purchase of items
# Copyright (C) 2020 Kamil 'konserw' Strzempowicz, konserw@gmail.com
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import logging
from datetime import date

from PySide2.QtCore import Slot, Qt, QDate
from PySide2.QtGui import QTextDocument, QFontDatabase
from PySide2.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PySide2.QtWidgets import QMainWindow, QDialog, QApplication, QCalendarWidget, QFileDialog

from forms.ui_mainwindow import Ui_MainWindow
from src.customer import CustomerSelectionDialog
from src.merchandise import MerchandiseSelectionDialog, DiscountDialog, DiscountGroupDialog
from src.offer import Offer
from src.terms import TermsChooserDialog, TermType
from src.user import User


class MainWindow(QMainWindow):
    def __init__(self, user: User):
        super().__init__()
        logging.debug("MainWindow creation")
        self.ui = Ui_MainWindow(self)
        self.retranslate_ui()
        self.set_offer_ui_enabled(False)

        self.font_database = QFontDatabase()
        self.font_database.addApplicationFont(':/font-regular')
        self.font_database.addApplicationFont(':/font-medium')
        self.font_database.addApplicationFont(':/font-bold')
        self.offer_font = self.font_database.font('Montserrat', 'Regular', 7)
        logging.info(f"Loaded font for offer print: {self.offer_font.family()} {self.offer_font.styleName()}")

        self.offer = None
        self.user = user
        self.calendar = QCalendarWidget()

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
        self.ui.push_button_discount_group.clicked.connect(self.set_discount_group)

        self.ui.command_link_button_customer.clicked.connect(self.select_customer)
        self.ui.check_box_query_date.stateChanged.connect(self.inquiry_date_toggled)
        self.ui.line_edit_query_date.textChanged.connect(self.inquiry_date_text_changed)
        self.ui.push_button_query_date.clicked.connect(self.inquiry_date_button_clicked)
        self.ui.check_box_query_number.stateChanged.connect(self.inquiry_number_toggled)
        self.ui.line_edit_query_number.textChanged.connect(self.inquiry_number_changed)

        self.ui.command_link_button_delivery.clicked.connect(self.select_delivery_terms)
        self.ui.command_link_button_offer.clicked.connect(self.select_offer_terms)
        self.ui.command_link_button_billing.clicked.connect(self.select_billing_terms)
        self.ui.command_link_button_delivery_date.clicked.connect(self.select_delivery_date_terms)
        self.ui.plain_text_edit_remarks.textChanged.connect(self.update_remarks)

        # must be connected at the end or will break tests
        self.calendar.clicked.connect(self.inquiry_date_changed)

    def retranslate_ui(self) -> None:
        self.ui.menu_offer.setTitle(self.tr("Offer"))
        self.ui.menu_export.setTitle(self.tr("Export"))
        self.ui.menu_help.setTitle(self.tr("Help"))
        self.ui.action_new.setText(self.tr("New"))
        self.ui.action_open.setText(self.tr("Open"))
        self.ui.action_save.setText(self.tr("Save"))
        self.ui.action_exit.setText(self.tr("Exit"))
        self.ui.action_PDF.setText(self.tr("PDF"))
        self.ui.action_print.setText(self.tr("Print preview"))
        self.ui.action_about.setText(self.tr("About"))
        self.ui.action_about_Qt.setText(self.tr("About Qt"))
        self.ui.action_new_number.setText(self.tr("Set new offer symbol"))
        self.ui.push_button_add_merchandise.setText(self.tr("Add merchandise"))
        self.ui.push_button_discount.setText(self.tr("Set Discount"))
        self.ui.push_button_discount_group.setText(self.tr("Set Discount for group"))
        self.ui.push_button_remove_row.setText(self.tr("Remove row"))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab), self.tr("Offer table"))
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_2), self.tr("Other information"))
        self.ui.command_link_button_customer.setText(self.tr("Choose customer"))
        self.ui.grup_box_query.setTitle(self.tr("Inquiry"))
        self.ui.check_box_query_date.setText(self.tr("Inquiry date:"))
        self.ui.push_button_query_date.setText("")
        self.ui.check_box_query_number.setText(self.tr("Inquiry number:"))
        self.ui.groupBox.setTitle(self.tr("Other information"))
        self.ui.command_link_button_delivery.setText(self.tr("Shipment terms"))
        self.ui.command_link_button_delivery_date.setText(self.tr("Delivery date"))
        self.ui.command_link_button_billing.setText(self.tr("Billing terms"))
        self.ui.command_link_button_offer.setText(self.tr("Offer terms"))
        self.ui.command_link_button_remarks.setText(self.tr("Remarks"))
#        self.ui.kolumny.setTitle(self.tr("Uk\u0142ad wydruku:"))
#        self.ui.check_box_no_column.setText(self.tr("LP"))
#        self.ui.check_box_merchandise_column.setText(self.tr("Towar"))
#        self.ui.check_box_details_column.setText(self.tr("Specyfikacja"))
#        self.ui.check_box_list_price_column.setText(self.tr("Cena katalogowa"))
#        self.ui.check_box_discount_column.setText(self.tr("Rabat"))
#        self.ui.check_box_price_column.setText(self.tr("Cena"))
#        self.ui.check_box_quantity_column.setText(self.tr("Ilo\u015b\u0107"))
#        self.ui.check_box_total_column.setText(self.tr("Warto\u015b\u0107"))

    def set_offer_ui_enabled(self, enable: bool) -> None:
        # menus
        self.ui.menu_export.setEnabled(enable)
        self.ui.action_save.setEnabled(enable)
        self.ui.action_new_number.setEnabled(enable)
        # tabs
        self.ui.tab.setEnabled(enable)
        self.ui.tab_2.setEnabled(enable)

    def update_inquiry_text(self) -> None:
        self.ui.plain_text_edit_query.setPlainText(self.offer.inquiry_text)

    @Slot()
    def new_offer(self) -> None:
        self.offer = Offer.create_empty(self.user, self)
        self.set_offer_ui_enabled(True)
        self.setWindowTitle(f"pyOffer - {self.offer.symbol}")
        self.ui.tableView.setModel(self.offer.merchandise_list)
        self.update_inquiry_text()

    @Slot()
    def new_offer_symbol(self) -> None:
        self.offer.new_symbol()
        self.setWindowTitle(f"pyOffer - {self.offer.symbol}")

    @Slot()
    def select_customer(self) -> None:
        dialog = CustomerSelectionDialog.make(self)
        if dialog.exec_() == QDialog.Accepted and dialog.chosen_customer:
            self.ui.plain_text_edit_customer.setPlainText(dialog.chosen_customer.description)
            self.offer.customer = dialog.chosen_customer

    @Slot()
    def update_remarks(self) -> None:
        self.offer.remarks = self.ui.plain_text_edit_remarks.toPlainText()

    @Slot()
    def select_delivery_terms(self) -> None:
        term_type = TermType.delivery
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec_() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_offer_terms(self) -> None:
        term_type = TermType.offer
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec_() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_offer.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_billing_terms(self) -> None:
        term_type = TermType.billing
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec_() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_billing.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_delivery_date_terms(self) -> None:
        term_type = TermType.delivery_date
        dialog = TermsChooserDialog.make(term_type, self)
        if dialog.exec_() == QDialog.Accepted and dialog.chosen_item:
            self.ui.plain_text_edit_delivery_date.setPlainText(dialog.chosen_item.long_desc)
            self.offer.terms[term_type] = dialog.chosen_item

    @Slot()
    def select_merchandise(self) -> None:
        dialog = MerchandiseSelectionDialog.make(self)
        dialog.exec_()
        for item in dialog.selected.values():
            self.offer.merchandise_list.change_item_count(item)

    @Slot()
    def remove_row(self) -> None:
        index = self.ui.tableView.currentIndex()
        if index.row() < self.offer.merchandise_list.rowCount():
            self.offer.merchandise_list.removeRow(index.row())

    @Slot()
    def set_discount(self) -> None:
        dialog = DiscountDialog(self)
        dialog.line_edit_expression.textChanged.connect(self.offer.merchandise_list.select_items)
        self.offer.merchandise_list.select_items("")
        if dialog.exec_() == QDialog.Accepted:
            self.offer.merchandise_list.apply_discount(dialog.discount_value)
        else:
            self.offer.merchandise_list.select_items(None)

    @Slot()
    def set_discount_group(self) -> None:
        dialog = DiscountGroupDialog(self.offer.merchandise_list.get_discount_groups(), self)
        dialog.selectionChanged.connect(self.offer.merchandise_list.select_items)
        if dialog.exec_() == QDialog.Accepted:
            self.offer.merchandise_list.apply_discount(dialog.discount_value)
        else:
            self.offer.merchandise_list.select_items(None)

    @Slot()
    def inquiry_date_button_clicked(self) -> None:
        self.ui.check_box_query_date.setChecked(Qt.Checked)
        self.calendar.show()

    @Slot(QDate)
    def inquiry_date_changed(self, d: QDate) -> None:
        self.ui.line_edit_query_date.setText(f"{d.toPython():%d.%m.%Y}")
        self.calendar.close()

    @Slot(int)
    def inquiry_date_toggled(self, state: int) -> None:
        enabled = state == Qt.Checked
        self.ui.line_edit_query_date.setEnabled(enabled)
        if enabled:
            self.ui.line_edit_query_date.setText(f"{date.today():%d.%m.%Y}")
        else:
            self.ui.line_edit_query_date.clear()

    @Slot(str)
    def inquiry_date_text_changed(self, text: str) -> None:
        self.offer.inquiry_date = text
        self.update_inquiry_text()

    @Slot(int)
    def inquiry_number_toggled(self, state: int) -> None:
        enabled = state == Qt.Checked
        self.ui.line_edit_query_number.setEnabled(enabled)
        if not enabled:
            self.ui.line_edit_query_number.clear()

    @Slot(str)
    def inquiry_number_changed(self, text: str) -> None:
        self.offer.inquiry_number = text
        self.update_inquiry_text()

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

    @Slot(QPrinter)
    def print(self, printer: QPrinter) -> None:
        margin = 5
        printer.setPageSize(QPrinter.A4)
        printer.setPageMargins(margin, margin, margin, margin, QPrinter.Millimeter)
        printer.setResolution(96)

        doc = QTextDocument()
        doc.setUseDesignMetrics(True)
        doc.setDefaultFont(self.offer_font)
        doc.setHtml(self.offer.document)
        doc.setPageSize(printer.pageRect().size())
        doc.print_(printer)

    @Slot()
    def print_preview(self) -> None:
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.NativeFormat)

        dialog = QPrintPreviewDialog(printer, self)
        dialog.setWindowFlags(Qt.Window)
        dialog.paintRequested.connect(self.print)
        dialog.showMaximized()
        dialog.exec_()

    @Slot()
    def print_pdf(self) -> None:
        file_name = QFileDialog.getSaveFileName(self, self.tr("Save to .pdf"), filter=self.tr("Portable Document Format (*.pdf)"))[0]
        if not file_name:
            return

        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)
        self.print(printer)

    @Slot()
    def about(self) -> None:
        pass

    @Slot()
    def about_qt(self) -> None:
        """Forward to QApplication.aboutQt, but keep here for sake of tests"""
        QApplication.aboutQt()
