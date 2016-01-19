#! coding:utf-8
"""
013_Transactions.py
トランザクションのコミットについて

トランザクション(取引)
トランザクションは，データベース操作の最小単位である．
もし格トランザクションがエラーの場合にはロールバックメソッドが実行され，トランザクションはキャンセルされる．
また，トランザクションはコミットする必要がある．
事前にオートコミットのオプションをつけることでコミットする必要がなくなる．


Created by 0160929 on 2016/01/19 16:01
"""
import psycopg2
import sys

con = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    con.autocommit = True

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Friends")
    cur.execute("CREATE TABLE Friends(Id serial PRIMARY KEY, Name VARCHAR(10))")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Tom')")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Rebecca')")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Jim')")
    cur.execute("INSERT INTO Friends(Name) VALUES ('Robert')")

    # commitしないとDBには反映されない
    # con.commit()


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

    con = None
    cur = None
    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    # DBにインポートできているか確認
    cur.execute("SELECT * FROM Friends")
    rows = cur.fetchall()
    for row in rows:
        print row