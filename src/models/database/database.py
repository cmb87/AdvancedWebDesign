import sqlite3 as lite
import sys
import uuid


class Database(object):
    def __init__(self):
        self.database = 'test.db'
        self.columnNames = None

    def _checkIfTableExists(self, tablename):
        """
        """
        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(tablename))
            if cur.fetchone()[0] == 1:
                return True
        return False

    def delete_table(self, tablename):
        """
        """
        con = lite.connect(self.database)
        with con:
            # From the connection, we get the cursor object. The cursor is used
            # to traverse the records from the result set. We call the execute()
            # method of the cursor and execute the SQL statement.
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS {}".format(tablename))
            print("-> Table removed!")

    def create_table(self, tablename, columnsdict, purge=False):
        """
        Create table
        columnsdict must be of the form
        columns = {"id": "INT", "name": "TEXT", "price": "INT"}
        """
        columns = ["{} {}".format(key, columnsdict[key]) for key in columnsdict.keys()]

        if not self._checkIfTableExists(tablename):
            self.columnNames = list(columnsdict.keys())
            con = lite.connect(self.database)
            with con:
                # From the connection, we get the cursor object. The cursor is used
                # to traverse the records from the result set. We call the execute()
                # method of the cursor and execute the SQL statement.
                cur = con.cursor()
                cur.execute("CREATE TABLE {}({})".format(tablename, ', '.join(columns)))
                print("-> Table created!")
        else:
            self.columnNames = self.getColumnNames(tablename)
            print("-> Table exists omitting!")

    def insert(self, tablename, rows, columnNames=None):
        """
        Insert multiple entries
        """
        placeholder = ', '.join(len(rows[0]) * ['?'])
        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            if isinstance(columnNames, type(None)):
                cur.executemany("INSERT INTO {} VALUES({})".format(tablename, placeholder), rows)
            elif isinstance(columnNames, list):
                cur.executemany("INSERT INTO {}({}) VALUES({})".format(tablename, ", ".join(columnNames), placeholder), rows)
                # self.lastRowID = cur.lastrowid

    def getColumnNames(self, tablename):
        """
        Get ColumnsNames of DB
        """
        con = lite.connect(self.database)
        with con:
            con.row_factory = lite.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM {}".format(tablename))
            return cur.fetchone().keys()

    def fetch(self, tablename, columns=None, query=None):
        """
        """
        columns = Database.columnsParser(columns)
        query = Database.queryParser(query)

        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            con.row_factory = lite.Row
            cur.execute("SELECT {} FROM {} {}".format(columns, tablename, query))
            return cur.fetchall()

    def remove(self, tablename, query=None):
        """
        """
        query = Database.queryParser(query)

        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            cur.execute("DELETE FROM {} {}".format(tablename, query))

    def getMetaData(self, tablename):
        """
        """
        con = lite.connect(self.database)
        with con:

            cur = con.cursor()
            cur.execute("PRAGMA table_info({})".format(tablename))
            data = cur.fetchall()
            return data

    @staticmethod
    def queryParser(query):
        if isinstance(query, type(None)):
            query = ''
        elif isinstance(query, str):
            query = 'WHERE ' + query
        return query

    @staticmethod
    def columnsParser(columns):
        if isinstance(columns, type(None)):
            columns = '*'
        elif isinstance(columns, list):
            columns = ', '.join(columns)
        return columns


if __name__ == "__main__":
    db = Database()

    columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT", "price": "INT"}
    db.delete_table("cars")
    db.create_table("cars", columns)

    db.insert("cars", (("Audi", 3000), ("VW", 1000)), columnNames=["name", "price"])
    db.insert("cars", ((5, "Hummer", 3000),))

    db.remove("cars", query="name = 'Hummer'")
    rows = db.fetch("cars", columns=['name', 'rowid'], query="price < 200000")
    print(rows)
