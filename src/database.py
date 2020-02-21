import logging
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class Database:
    def __init__(self):
        self.database = QSqlDatabase.addDatabase("QPSQL")
        self.database.setHostName("127.0.0.1")
        self.database.setDatabaseName("koferta_test")
        self.database.setUserName("postgres")
        self.database.setPassword("docker")
        if not self.database.open():
            logging.error("Failed to open database")
            logging.error(self.database.lastError().text())

    @staticmethod
    def get_customers_table():
        model = QSqlTableModel()
        model.setTable("customers_view")
        model.select()

    @staticmethod
    def get_terms_table(term_type):
        model = QSqlTableModel()
        model.setTable("terms_{}".format(term_type.name))
        model.select()
        while model.canFetchMore():
            model.fetchMore()
        return model
