import logging
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from src.terms import TermType


class Database:
    TERM_TABLE = {
        TermType.billing: "billingTerms",
        TermType.delivery: "deliveryTerms",
        TermType.delivery_date: "deliveryDateTerms",
        TermType.offer: "offerTerms"
    }

    def __init__(self):
        self.database = QSqlDatabase.addDatabase("QPSQL")
        self.database.setHostName("127.0.0.1")
        self.database.setDatabaseName("koferta_test")
        self.database.setUserName("postgres")
        self.database.setPassword("docker")
        if not self.database.open():
            logging.error("Failed to open database")
            logging.error(self.database.lastError().text())

    def get_terms_table(self, term_type):
        model = QSqlTableModel()
        model.setTable(self.TERM_TABLE[term_type])
        model.select()
        while model.canFetchMore():
            model.fetchMore()
        return model
