import sqlite3 as lite
import sys
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)-8s] [%(name)-8s] [%(levelname)-1s] [%(message)s]')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def queryop(key, op):
    val, operator = op[1], op[0]
    if isinstance(val, str):
        val = "'{}'".format(val)
    return "({} {} {})".format(key, operator, val)


class Database(object):
    def __init__(self, dbpath):
        self.database = dbpath
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
        try:
            with con:
                # From the connection, we get the cursor object. The cursor is used
                # to traverse the records from the result set. We call the execute()
                # method of the cursor and execute the SQL statement.
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS {}".format(tablename))
                logger.info("Deleting table {}.".format(tablename))

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

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
            try:
                with con:
                    # From the connection, we get the cursor object. The cursor is used
                    # to traverse the records from the result set. We call the execute()
                    # method of the cursor and execute the SQL statement.
                    cur = con.cursor()
                    cur.execute("CREATE TABLE {}({})".format(tablename, ', '.join(columns)))
                    logger.info("New table {} created sucessfully.".format(tablename))

            except lite.Error as e:
                logger.warning("{}".format(e))
            except Exception as e:
                logger.warning("{}".format(e))
        else:
            self.columnNames = self.getColumnNames(tablename)
            logger.info("Table {} already exists. Reusing...".format(tablename))

    def insertMany(self, tablename, rows, columnNames=None):
        """
        Insert multiple entries
        db.insertMany("cars", (("Audi", 3000), ("VW", 1000)), columnNames=["name", "price"])
        db.insertMany("cars", ((5, "Hummer2", 3000), (6, "Audi", 4000)))
        """
        placeholder = ', '.join(len(rows[0]) * ['?'])
        con = lite.connect(self.database)
        try:
            with con:
                cur = con.cursor()
                if isinstance(columnNames, type(None)):
                    cur.executemany("INSERT INTO {} VALUES({})".format(tablename, placeholder), rows)
                elif isinstance(columnNames, list):
                    cur.executemany("INSERT INTO {}({}) VALUES({})".format(tablename, ", ".join(columnNames), placeholder), rows)

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

    def insert(self, tablename, rows):
        """
        Insert a list of dictionaries
        """
        con = lite.connect(self.database)
        for row in rows:
            placeholders = ', '.join(['?' for key, val in row.items()])
            vals = [val for key, val in row.items()]
            keys = list(row.keys())

            try:
                with con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO {}({}) VALUES({})".format(tablename, ', '.join(keys), placeholders), vals)

            except lite.Error as e:
                logger.warning("{}".format(e))
            except Exception as e:
                logger.warning("{}".format(e))

    def getColumnNames(self, tablename):
        """
        Get ColumnsNames of DB
        """
        con = lite.connect(self.database)
        try:
            with con:
                con.row_factory = lite.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM {}".format(tablename))
                return cur.fetchone().keys()

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

    def find_one(self, tablename, query):
        """
        """

        query = ' AND '.join(list(map(queryop, query.keys(), query.values())))

        con = lite.connect(self.database)
        try:
            with con:
                con.row_factory = lite.Row
                cur = con.cursor()
                cur.execute("SELECT {} FROM {} WHERE {}".format('*', tablename, query))
                return dict(cur.fetchone())

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

    def find(self, tablename, query):
        """Summary

        Args:
            tablename (TYPE): Description
            query (TYPE): Description

        Returns:
            TYPE: Description
        """
        query = ' AND '.join(list(map(queryop, query.keys(), query.values())))

        con = lite.connect(self.database)
        try:
            with con:
                con.row_factory = lite.Row
                cur = con.cursor()
                cur.execute("SELECT {} FROM {} WHERE {}".format('*', tablename, query))
                return list(map(dict, cur.fetchall()))

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

    def remove(self, tablename, query):
        """
        Args:
            tablename (TYPE): Description
            query (TYPE): Description
        """
        query = ' AND '.join(list(map(queryop, query.keys(), query.values())))

        con = lite.connect(self.database)
        try:
            with con:
                cur = con.cursor()
                cur.execute("DELETE FROM {} WHERE {}".format(tablename, query))

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

    def getMetaData(self, tablename):
        """
        Args:
            tablename (TYPE): Description

        Returns:
            TYPE: Description
        """

        con = lite.connect(self.database)
        try:
            with con:

                cur = con.cursor()
                cur.execute("PRAGMA table_info({})".format(tablename))
                return cur.fetchall()

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))


if __name__ == "__main__":

    db = Database('test2.db')

    columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT", "price": "INT"}

    # db.delete_table("cars")
    db.create_table("cars", columns)

    db.insert("cars", [{"name": "Seat123", "price": 300},
                       {"name": "VW", "price": 600},
                       {"name": "Skoda", "price": 10000},
                       {"name": "Porsche", "price": 600}])

    db.remove("cars", query={"name": ["=", "Audi"], "price": ["<=", 3000]})

    rows = db.find("cars", query={"name": ["=", "VW"]})

    print(rows)
