#! coding:utf-8
"""
006_ParameterizedQueries.py
Dict型でのQuery生成方法

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
    # 辞書方で取得
    cur = con.cursor()

    uId = 1
    uPrice = 62300
    cur.execute("UPDATE Cars SET Price=%s WHERE Id=%s", (uPrice, uId))
    con.commit()
    # 辞書型でパース
    cur.execute("SELECT * FROM Cars WHERE Id=%(id)s", {'id': uId})
    con.commit()

    print "Number of rows updated: %d" % cur.rowcount


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
