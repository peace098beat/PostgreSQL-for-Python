#! coding:utf-8
"""
003_ConvenienceExecutemanyMethod.py
Queryを生成するexecutemany関数の使い方

[参考](http://zetcode.com/db/postgresqlpythontutorial/)

"""
import psycopg2
import sys

cars = {
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600),
}

con = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    # Create a 'Cars' table
    cur.execute("DROP TABLE IF EXISTS Cars")
    # Create a 'Cars' table
    cur.execute("CREATE TABLE Cars("
                "Id INTEGER PRIMARY KEY, "
                "Name VARCHAR(20), "
                "Price INT"
                ")")

    # ******************************************************************
    # Insert rows
    query = "INSERT INTO Cars (Id, Name, Price) VALUES (%s, %s, %s)"
    cur.executemany(query, cars)
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
