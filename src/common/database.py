import sqlite3 as lite
import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../'))

import src.common.constants as DBCONSTANTS

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

    PATH2DB = DBCONSTANTS.DATABASEPATH

    @staticmethod
    def _checkIfTableExists(tablename):

        con = lite.connect(Database.PATH2DB)

        try:
            with con:
                cur = con.cursor()
                cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{}'".format(tablename))
                if cur.fetchone()[0] == 1:
                    return True
        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

        return False

    @staticmethod
    def delete_table(tablename):
        """
        """
        con = lite.connect(Database.PATH2DB)
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

    @staticmethod
    def create_table(tablename, columnsdict):
        """
        Create table
        columnsdict must be of the form
        columns = {"id": "INT", "name": "TEXT", "price": "INT"}
        """
        columns = ["{} {}".format(key, columnsdict[key]) for key in columnsdict.keys()]

        if not Database._checkIfTableExists(tablename):
            con = lite.connect(Database.PATH2DB)
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
            logger.info("Table {} already exists. Reusing...".format(tablename))

    @staticmethod
    def insertMany(self, tablename, rows, columnNames=None):
        """
        Insert multiple entries
        db.insertMany("cars", (("Audi", 3000), ("VW", 1000)), columnNames=["name", "price"])
        db.insertMany("cars", ((5, "Hummer2", 3000), (6, "Audi", 4000)))
        """
        placeholder = ', '.join(len(rows[0]) * ['?'])
        con = lite.connect(Database.PATH2DB)
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

    @staticmethod
    def insert(tablename, rows):
        """
        Insert a list of dictionaries
        """
        con = lite.connect(Database.PATH2DB)
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

    @staticmethod
    def getColumnNames(tablename):
        """
        Get ColumnsNames of DB
        """
        con = lite.connect(Database.PATH2DB)
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

    @staticmethod
    def find_one(tablename, query):
        """
        """

        query = ' AND '.join(list(map(queryop, query.keys(), query.values())))

        con = lite.connect(Database.PATH2DB)
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

    @staticmethod
    def find(tablename, query):
        """Summary

        Args:
            tablename (TYPE): Description
            query (TYPE): Description

        Returns:
            TYPE: Description
        """
        query = ' AND '.join(list(map(queryop, query.keys(), query.values())))

        con = lite.connect(Database.PATH2DB)
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

    @staticmethod
    def remove(tablename, query):
        """
        Args:
            tablename (TYPE): Description
            query (TYPE): Description
        """
        query = ' AND '.join(list(map(queryop, query.keys(), query.values())))

        con = lite.connect(Database.PATH2DB)
        try:
            with con:
                cur = con.cursor()
                cur.execute("DELETE FROM {} WHERE {}".format(tablename, query))

        except lite.Error as e:
            logger.warning("{}".format(e))
        except Exception as e:
            logger.warning("{}".format(e))

    @staticmethod
    def getMetaData(tablename):
        """
        Args:
            tablename (TYPE): Description

        Returns:
            TYPE: Description
        """

        con = lite.connect(Database.PATH2DB)
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

    columns = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT", "price": "INT"}

    # db.delete_table("cars")
    Database.create_table("cars", columns)

    Database.insert("cars", [{"name": "Seat123", "price": 300},
                             {"name": "VW", "price": 600},
                             {"name": "Skoda", "price": 10000},
                             {"name": "Porsche", "price": 600}])

    Database.remove("cars", query={"name": ["=", "Audi"], "price": ["<=", 3000]})

    rows = Database.find("cars", query={"name": ["=", "VW"]})

    print(rows)