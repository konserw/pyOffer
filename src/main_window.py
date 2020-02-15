from PyQt5.QtWidgets import QMainWindow, QDialog

from src.terms import TermChooserDialogFactory, TermType
from src.database import Database

from generated.MainWindow_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.db = Database()
        self.term_chooser_factory = TermChooserDialogFactory(self, self.db)

        self.ui.commandLinkButton_klient.clicked.connect(self.select_customer)
        self.ui.commandLinkButton_offerTerms.clicked.connect(self.select_offer_terms)

    def select_customer(self):
        pass

    def select_offer_terms(self):
        dialog = self.term_chooser_factory.get_terms_chooser_dialog(TermType.offer)
        if dialog.exec() == QDialog.Accepted:
            self.ui.plainTextEdit_oferta.setPlainText(dialog.choosen_item.long_desc)
