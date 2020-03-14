from PySide2.QtWidgets import QMainWindow, QDialog

from generated.ui_mainwindow import Ui_MainWindow
from src.customer import CustomerFactory
from src.database import Database
from src.merchandise import MerchandiseListModel, create_merchandise_selection_dialog
from src.terms import TermChooserDialogFactory, TermType


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()
        self.merchandise_list_model = MerchandiseListModel(self.db, self)
        self.ui.tableView.setModel(self.merchandise_list_model)
        self.term_chooser_factory = TermChooserDialogFactory(self.db, self)
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
        for item_id, count in dialog.selected.items():
            self.merchandise_list_model.change_item_count(item_id, count)
