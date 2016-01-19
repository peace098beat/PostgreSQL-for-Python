#! coding:utf-8
"""
005_DictionaryCursor_fetchall_fetchone.py
辞書型でデータの取得

[参考](http://zetcode.com/db/postgresqlpythontutorial/)

"""

import psycopg2
import psycopg2.extras
import sys

con = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    # 辞書方で取得
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM Cars")

    rows = cur.fetchall()

    for row in rows:
        print "%s %s %s" % (row["id"], row["name"], row["price"])


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
