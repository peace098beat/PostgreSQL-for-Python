#! coding:utf-8
"""
007_InsertingImages.py
画像（バイナリ）データの格納

"""
import psycopg2
import sys


def readImage():
    try:
        fin = open("woman.jpg", "rb")
        img = fin.read()
        return img
    except IOError, e:
        print "-- Error readImage() --"
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        if fin:
            fin.close()


con = None

try:

    # (おまじない) DBに接続
    con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)

    # (おまじない) コネクションからカーソルオブジェクトを取得
    cur = con.cursor()

    data = readImage()
    binary = psycopg2.Binary(data)

    cur.execute("DROP TABLE IF EXISTS Images")
    cur.execute("CREATE TABLE Images (Id INT PRIMARY KEY, Data BYTEA)")
    cur.execute("INSERT INTO Images (Id, Data) VALUES (1, %s)", (binary,))

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
