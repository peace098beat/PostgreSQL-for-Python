#! coding:utf-8
"""
001_ConnectingDB.py
DBに接続しバージョン情報を取得

[参考](http://zetcode.com/db/postgresqlpythontutorial/)

"""
__version__ = '0.0'

import psycopg2
import sys

con = None

try:

    # DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # コネクションからカーソルオブジェクトを取得
    cur = con.cursor()
    # versionを取得
    cur.execute('SELECT version()')
    # SQLをexecuteして得られたデータをフェッチ
    ver = cur.fetchone()
    # ヴァージョンの表示
    print ver

    print psycopg2.__version__

except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:

    if con:
        con.close()
