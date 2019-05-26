import sqlite3 as lite
import sys


class Database(object):
    def __init__(self):
        self.database = 'test.db'

    def create_table(self, tablename, columnsdict, purge=False):
        """
        Create table
        columnsdict must be of the form
        columns = {"id": "INT", "name": "TEXT", "price": "INT"}
        """
        columns = ["{} {}".format(key, columnsdict[key]) for key in columnsdict.keys()]

        con = lite.connect(self.database)
        with con:
            # From the connection, we get the cursor object. The cursor is used
            # to traverse the records from the result set. We call the execute()
            # method of the cursor and execute the SQL statement.
            cur = con.cursor()
            if purge:
                cur.execute("DROP TABLE IF EXISTS {}".format(tablename))
            cur.execute("CREATE TABLE {}({})".format(tablename, ', '.join(columns)))

            print("-> Table created!")

    def insert(self, tablename, rows):
        """
        Insert multiple entries
        """
        for row in rows:
            assert len(row) == len(rows[0]), "Warning entries don't match!"
        placeholder = ', '.join(len(rows[0]) * ['?'])

        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO {} VALUES({})".format(tablename, placeholder), rows)
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

    def fetchAll(self, tablename, columns=None, query=None, mode="fetchall"):
        """
        """
        columnNames = self.getColumnNames(tablename)

        if isinstance(columns, type(None)):
            columns = '*'
        elif isinstance(columns, list):
            columns = ', '.join(columns)

        if isinstance(query, type(None)):
            query = ''
        if isinstance(query, str):
            query = 'WHERE ' + query

        con = lite.connect(self.database)
        with con:
            cur = con.cursor()
            if mode == "fetchall":
                con.row_factory = lite.Row
                cur.execute("SELECT {} FROM {} {}".format(columns, tablename, query))
                return cur.fetchall()
            elif mode == "fetchone":
                con.row_factory = lite.Row
                cur.execute("SELECT {} FROM {} {}".format(columns, tablename, query))
                return cur.fetchone()
            elif mode == "update":
                cur.execute("UPDATE {} SET price=? {}".format(tablename, query))
            else:
                print("Mode unknown")

    def getMetaData(self, tablename):
        """
        """
        con = lite.connect(self.database)
        with con:

            cur = con.cursor()
            cur.execute("PRAGMA table_info({})".format(tablename))
            data = cur.fetchall()
            return data


if __name__ == "__main__":
    db = Database()

    columns = {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "price": "INT"}

    db.create_table("cars", columns, purge=True)
    db.insert("cars", [(1, 'Audi', 52642),
                       (2, 'BMW', 51642),
                       (3, 'Hummer', 1642), ])

    rows = db.fetchAll("cars", columns=['name', 'id'], query="price < 100")
    print(rows)
