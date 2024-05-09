from server import Server
from options import Options
from mailbox import Mailbox
from sqlite_table import DbBase
from connection_pool import ConnectionPool


class MAIN:
    HOST = "localhost"
    PORT = 1201
    INFO = "version: 1.3"


if __name__ == "__main__":
    options_instance = Options(MAIN.INFO)

    db = DbBase(db_path="sqlite_db.db")
    db.connect()
    mailbox_instance = Mailbox(username=options_instance.logged_in_client)
    connection_pool = ConnectionPool(max_connections=10)
    server = Server(MAIN.HOST, MAIN.PORT, MAIN.INFO, options_instance, mailbox_instance, db, connection_pool)
    server.start()
