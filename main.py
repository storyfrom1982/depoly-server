import sys

import mysql.connector
import json

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python3 main.py user password jsonFile")
        exit(0)

    mydb = mysql.connector.connect(
        host="10.3.4.158",
        port=3306,
        user=sys.argv[1],
        password=sys.argv[2],
        db=sys.argv[1])

    js = {}
    s = ""
    json_file = sys.argv[3]

    with open(json_file, 'r') as load_f:
        # s = load_f.read()
        js = json.load(load_f)
        s = json.dumps(js)

    # Get a cursor
    cur = mydb.cursor()

    # Execute a query
    cur.execute("DROP TABLE IF EXISTS appNavi;")

    cur.execute("CREATE TABLE IF NOT EXISTS appNavi(id VARCHAR(255), json TEXT, PRIMARY KEY(id));")

    cur.execute("SHOW TABLES;")
    for x in cur:
        print(x)

    sql = "INSERT INTO appNavi (id, json) VALUES (%s, %s)"
    val = ("navi", s)
    cur.execute(sql, val)

    mydb.commit()

    cur.execute('SELECT * FROM appNavi')
    ret = cur.fetchall()

    for x in ret:
        print(x)

    # Close connection
    mydb.close()