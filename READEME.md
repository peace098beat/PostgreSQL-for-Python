
# PostgreSQL for Python
PostgreSQLをpsycopg2モジュールで利用するためのチュートリアルのまとめ.

[参考> Zetcode : PostgreSQL Python tutorial](http://zetcode.com/db/postgresqlpythontutorial/)

## 目次
 1. ConnectingDB.py
     - DBに接続しバージョン情報を取得
 2. InsertingData.py
     - DBにデータを追加
 3. ConvenienceExecutemanyMethod.py
     - Queryを生成するexecutemany関数の使い方
 4. RetrievingData.py
     - データの取得(fetchall(), fetchone())
 5. DictionaryCursor.py
     - 辞書型データの取得
 6. ParameterizedQueries.py
     - Dict型でのQuery生成方法
 7. InsertingImages.py
     - 画像（バイナリ）データの格納
 8. ReadingImages.py
     - 画像(バイナリ)の取得
 9. Metadata.py
     - カラムの詳細データの取得
 10. SystemInformationSchema.py
     - システム変数を使ってデータを取得
 11. ExportData.py
     - DBデータをtxt形式でエクスポート
 12. ImportData.py
     - DBデータをtxt形式でインポート
 13. Tranactions.py
     - トランザクションのコミットについて  

## 環境
- windows7 (64bit)
- Python2.7.112bit)
- psycopg2 2.6.1
- PostgreSQL 8.3.23, compiled by Visual C++ build 1400

## まとめ
```python

# ******************************************************************
# 接続
con = psycopg2.connect(dsn=None,
                           database='postgres', user='postgres', password='postgres', host='localhost', port=5432,
                           connection_factory=None, cursor_factory=None, async=False)
# カーソルオブジェクト
cur = con.cursor()
# versionを取得
cur.execute('SELECT version()')

# ******************************************************************
# SQLをexecuteして得られたデータをフェッチ
ver = cur.fetchone()
print ver
# psycopg2のヴァージョン表示
print psycopg2.__version__

# ******************************************************************
# テーブルの生成
cur.execute("CREATE TABLE Cars("
            "Id INTEGER PRIMARY KEY, "
            "Name VARCHAR(20), "
            "Price INT"
            ")")
            
# Insert rows
cur.execute("INSERT INTO Cars VALUES(1, 'Audi', 52642)")
cur.execute("INSERT INTO Cars VALUES(2, 'Mercedes', 57127)")
cur.execute("INSERT INTO Cars VALUES(3, 'Skoda', 9000)")

# The changes are committed to the database
con.commit()


# ******************************************************************
cars = {
    (1, 'Audi', 52642),
    (2, 'Mercedes', 57127),
    (3, 'Skoda', 9000),
    (4, 'Volvo', 29000),
    (5, 'Bentley', 350000),
    (6, 'Citroen', 21000),
    (7, 'Hummer', 41400),
    (8, 'Volkswagen', 21600),
}

# Insert rows
query = "INSERT INTO Cars (Id, Name, Price) VALUES (%s, %s, %s)"
cur.executemany(query, cars)


# ******************************************************************
cur.execute("SELECT * FROM Cars")

# Practice > fetchall()
rows = cur.fetchall()

for row in rows:
    print row

# ******************************************************************
cur.execute("SELECT * FROM Cars")

# Practice > fetchone()
while True:
    row = cur.fetchone()

    if row == None:
        break

    print row[0], row[1], row[2]


# ******************************************************************
# 辞書方で取得
cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur.execute("SELECT * FROM Cars")
rows = cur.fetchall()

for row in rows:
    print "%s %s %s" % (row["id"], row["name"], row["price"])

# ******************************************************************
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

# ******************************************************************
# 画像の保存
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

    cur = con.cursor()

data = readImage()
binary = psycopg2.Binary(data)

cur.execute("DROP TABLE IF EXISTS Images")
cur.execute("CREATE TABLE Images (Id INT PRIMARY KEY, Data BYTEA)")
cur.execute("INSERT INTO Images (Id, Data) VALUES (1, %s)", (binary,))

con.commit()
# ******************************************************************
# 画像の読み出し
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
            
cur = con.cursor()

data = readImage()
binary = psycopg2.Binary(data)

cur.execute("SELECT Data FROM Images LIMIT 1")
data = cur.fetchone()[0]

writeImage(data)     


# ******************************************************************
# カラムの詳細データの取得
cur = con.cursor()


cur.execute("SELECT * FROM Cars")

col_names = [cn[0] for cn in cur.description]
print  [cn for cn in cur.description]

rows = cur.fetchall()

print "%s %-10s %s" % (col_names[0], col_names[1], col_names[2])

for row in rows:
    print "%2s %-10s %s" % row

# ******************************************************************
# システム変数を使ってデータを取得
cur = con.cursor()

cur.execute("""SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'public'""")

rows = cur.fetchall()

for row in rows:
    print row[0]

# ******************************************************************
# DBデータをtxt形式でエクスポート
cur = con.cursor()

# 出力先ファイルの指定
fout = open('cars.csv', 'w')

# Carsテーブルを'~|'区切りで出力
cur.copy_to(fout, 'Cars', sep=",")


# ******************************************************************
# DBデータをtxt形式でインポート
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



# ******************************************************************
# 013_Transactions.py
# トランザクションのコミットについて

con.autocommit = True
con.commit()


```



## インストールについての参考資料

[Windows+Apache＋PHP＋PostgreSQLによるWebアプリケーション
－入門編－](http://www.yc.tcu.ac.jp/~yamada/doc/pgsql/index.html)

[Using psycopg2 with PostgreSQL](https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL)













