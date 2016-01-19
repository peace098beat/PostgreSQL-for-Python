#! coding:utf-8
"""
009_Metadata.py
カラムの詳細データの取得

cur.description
id name       price
 4 Volvo      29000
 5 Bentley    350000
 8 Volkswagen 21600
 7 Hummer     41400
 3 Skoda      9000
 6 Citroen    21000
 2 Mercedes   124600
 1 Audi       62300


Created by 0160929 on 2016/01/19 15:42
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

    col_names = [cn[0] for cn in cur.description]
    print  [cn for cn in cur.description]

    rows = cur.fetchall()

    print "%s %-10s %s" % (col_names[0], col_names[1], col_names[2])

    for row in rows:
        print "%2s %-10s %s" % row

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
