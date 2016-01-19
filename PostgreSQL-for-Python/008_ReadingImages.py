#! coding:utf-8
"""
008_ReadingImages
画像(バイナリ)の呼び出し

Created by 0160929 on 2016/01/19 15:40
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


def writeImage(data):

    try:
        fout = open('woman2.jpg','wb')
        fout.write(data)

    except IOError, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if fout:
            fout.close()


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

    cur.execute("SELECT Data FROM Images LIMIT 1")
    data = cur.fetchone()[0]

    writeImage(data)



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
