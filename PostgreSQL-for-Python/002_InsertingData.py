#! coding:utf-8
"""
002_InsertingData.py
DBにデータを追加

[参考](http://zetcode.com/db/postgresqlpythontutorial/)

"""

import psycopg2
import sys

con = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    # Create a 'Cars' table
    cur.execute("CREATE TABLE Cars("
                "Id INTEGER PRIMARY KEY, "
                "Name VARCHAR(20), "
                "Price INT"
                ")")
    # Insert rows
    # ******************************************************************
    cur.execute("INSERT INTO Cars VALUES(1, 'Audi', 52642)")
    cur.execute("INSERT INTO Cars VALUES(2, 'Mercedes', 57127)")
    cur.execute("INSERT INTO Cars VALUES(3, 'Skoda', 9000)")
    # ******************************************************************

    # The changes are committed to the database
    con.commit()

except psycopg2.DatabaseError, e:
    print "-- Error --"

    # In case of an error, we roll back any possible changes to our database table.
    if con:
        con.rollback()

    print 'Error %s' % e
    sys.exit(1)


finally:

    if con:
        con.close()
