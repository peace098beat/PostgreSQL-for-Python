#! coding:utf-8
"""
004_RetrievingData.py
データの取得(fetchall(), fetchone())

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
    cur.execute("SELECT * FROM Cars")



    # ******************************************************************
    cur.execute("SELECT * FROM Cars")

    print "= Practice > fetchall() ="
    rows = cur.fetchall()

    for row in rows:
        print row

    # ******************************************************************
    cur.execute("SELECT * FROM Cars")

    print "= Practice > fetchone() ="
    while True:
        row = cur.fetchone()

        if row == None:
            break

        print row[0], row[1], row[2]


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
