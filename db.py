import sqlite3
from log import LogManager

class DB:
    def __init__(self, db_name='client.db'):
        self.db_name = db_name
        self._create_table()
        self.log = LogManager()

    def _connect(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                cname varchar(255) UNIQUE NOT NULL,
                cvalue varchar(255)  NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def insert(self, identifier, value):
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO config (cvalue, cresult) VALUES (?, ?)", (identifier, value))
            conn.commit()
        except sqlite3.IntegrityError as e:
            self.log.write("Erro ao inserir:", e)
        finally:
            conn.close()

    def query(self, identifier):
        conn = self._connect()
        cursor = conn.cursor()

        if identifier:
            cursor.execute("SELECT * FROM config WHERE cvalue = ?", ('%' + identifier + '%',))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def delete(self, identifier):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM config WHERE cname = ?", (identifier,))
        conn.commit()
        conn.close()
