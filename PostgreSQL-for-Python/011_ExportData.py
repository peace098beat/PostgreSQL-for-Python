#! coding:utf-8
"""
011_ExportData.py
DBデータをtxt形式でエクスポート
Created by 0160929 on 2016/01/19 15:54
"""

import psycopg2
import sys

con = None
fout = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    # 出力先ファイルの指定
    fout = open('cars.csv', 'w')

    # Carsテーブルを'~|'区切りで出力
    cur.copy_to(fout, 'Cars', sep=",")

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

    if fout:
        fout.close()
