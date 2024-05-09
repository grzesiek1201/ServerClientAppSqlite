import sqlite3


class DbBase:
    def __init__(self, db_path):
        self.db_name = db_path
        self.connection = None
        self.connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_server_close()

    def connect(self):
        if not self.connected or (self.connection and self.connection.closed):
            try:
                self.connection = sqlite3.connect(self.db_name)
                self.connection.execute("PRAGMA foreign_keys = 1")
                self.connection.row_factory = sqlite3.Row
                self.connected = True
                print("Connected to SQLite database.")
            except sqlite3.Error as e:
                print(f"Error while connecting to SQLite: {e}")
                self.connection = None

        return self.connection
    def close_connection(self):
        if self.connected:
            self.connection.close()
            print("SQLite connection closed.")
            self.connected = False

    def execute_sql(self, sql, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            self.connection.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error executing SQL query: {e}")
            raise e


    def db_server_start(self):
        try:
            self.execute_sql("CREATE TABLE IF NOT EXISTS UsersBase (id INTEGER PRIMARY KEY,username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'USER')")
            self.execute_sql("CREATE TABLE IF NOT EXISTS UsersMessages (sender TEXT NOT NULL, recipient TEXT NOT NULL, message TEXT NOT NULL)")
            print("Tables created successfully.")
        except sqlite3.Error as e:
            print("Error while creating tables:", e)

    def register_user(self, username, password):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "INSERT INTO UsersBase (username, password) VALUES (?, ?)"
            params = (username, password)
            cursor = self.execute_sql(sql, params)
            if cursor:
                self.connection.commit()
                return "Registration successful."
            else:
                return "Failed to register user."
        except sqlite3.Error as e:
            print("Error registering user:", e)
            raise e

    def authenticate_user(self, username, password):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "SELECT role FROM UsersBase WHERE username = ? AND password = ?"
            params = (username, password)
            cursor = self.execute_sql(sql, params)
            role = cursor.fetchone()
            print(f"SQL Query: {sql}")
            print(f"Params: {params}")
            print(f"Retrieved Role: {role}")
            return role[0] if role else None
        except sqlite3.Error as e:
            print(f"Error during authentication: {str(e)}")
            return None

    def get_user_role(self, username):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "SELECT role FROM UsersBase WHERE username = ?"
            params = (username,)
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                role = cursor.fetchone()
                return role[0] if role else None
        except sqlite3.Error as e:
            raise e

    def delete_user(self, username):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "DELETE FROM UsersBase WHERE username = ?"
            params = (username,)
            self.execute_sql(sql, params)
        except sqlite3.Error as e:
            self.connection.rollback()
            raise e

    def send_message(self, sender, recipient, message):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "INSERT INTO UsersMessages (sender, recipient, message) VALUES (?, ?, ?)"
            params = (sender, recipient, message)
            self.execute_sql(sql, params)
            return "Message sent."
        except sqlite3.Error as e:
            print(f"Error sending message: {str(e)}")
            return f"Error sending message: {str(e)}"

    def read_messages(self, username):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "SELECT sender, message FROM UsersMessages WHERE recipient = ?"
            params = (username,)
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            messages = cursor.fetchall()
            cursor.close()
            return messages
        except sqlite3.Error as e:
            print(f"Error reading messages: {str(e)}")
            return f"Error reading messages: {str(e)}"

    def show_all_messages(self, recipient):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "SELECT sender, message FROM UsersMessages WHERE recipient = ?"
            params = (recipient,)
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                messages = cursor.fetchall()
                return messages
        except sqlite3.Error as e:
            raise e

    def show_all_users(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            sql = "SELECT username, role FROM UsersBase"
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                users = cursor.fetchall()
                return users
        except sqlite3.Error as e:
            raise e

    def db_server_close(self):
        self.close_connection()
        print('Server DB - CLOSED')


if __name__ == "__main__":
    db_name = r"C:\Users\gzywi\PycharmProjects\ServerClientApp\sqlite_db.db"
    with DbBase(db_name) as db:
        db.db_server_start()
