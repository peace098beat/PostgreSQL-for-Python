#! coding:utf-8
"""
012_ImportData.py
DBデータをtxt形式でインポート

"""

import psycopg2
import sys

con = None
fin = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    cur.execute("DELETE FROM Cars")

    # 出力先ファイルの指定
    fin = open('cars.csv', 'r')

    # Carsテーブルを','区切りで入力
    cur.copy_from(fin, 'Cars', sep=",")

    # DBにインポートできているか確認
    cur.execute("SELECT * FROM Cars")
    rows = cur.fetchall()
    for row in rows:
        print row

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

    if fin:
        fin.close()
