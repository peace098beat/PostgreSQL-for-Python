#! coding:utf-8
"""
010_SystemInformationSchema.py
システム変数を使ってデータを取得
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'
    cars
    images
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

    cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")

    rows = cur.fetchall()

    for row in rows:
        print row[0]


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
